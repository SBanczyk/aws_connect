import os
import time
import boto3
import botocore.exceptions
import psycopg2
from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

for db_connect_attempts in range(10):
    try:
        db_connect = psycopg2.connect(
            host=os.environ["DB_IP"],
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PWD"],
        )
    except psycopg2.OperationalError as error:
        print(error)
        time.sleep(1)
    else:
        break


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    disabled: bool | None = None
    resource_groups: list


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    with db_connect.cursor() as cursor:
        cursor.execute("SELECT * from users where username=%s", (username,))
        row = cursor.fetchone()
        if row is not None:
            user_dict = {
                "username": row[0],
                "hashed_password": row[1],
                "disabled": row[2],
                "resource_groups": [],
            }
        else:
            return
        cursor.execute(
            "select RG.resource_group_name "
            "from roles R join users_roles UR on UR.role_name = R.role_name "
            "join roles_resource_groups RSG on R.role_name = RSG.role_name "
            "join resource_groups RG on RSG.resource_group = RG.resource_group_name "
            "where UR.username=%s", (username,),
        )
        row = cursor.fetchone()
        while row is not None:
            user_dict["resource_groups"].append(row[0])
            row = cursor.fetchone()
        return UserInDB(**user_dict)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def user_in_resource_groups(
    current_user: Annotated[User, Depends(get_current_active_user)], instance
):
    for tag in instance.tags:
        if tag["Key"] == "resource_group":
            if tag["Value"] not in current_user.resource_groups:
                return False
            else:
                return True


session = boto3.Session(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    region_name=os.environ["REGION_NAME"],
)
ec2 = session.resource("ec2")


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/instances/{instance_id}/state")
async def state(
    current_user: Annotated[User, Depends(get_current_active_user)], instance_id: str
):
    try:
        instance = ec2.Instance(instance_id)
        if not user_in_resource_groups(current_user, instance):
            raise HTTPException(status_code=403)
        else:
            return instance.state
    except botocore.exceptions.ClientError as err:
        if "InvalidInstanceID" in err.response["Error"]["Code"]:
            raise HTTPException(status_code=404, detail="Invalid instance id")
        else:
            raise err


@app.post("/instances/{instance_id}/start", status_code=204)
async def start(
    current_user: Annotated[User, Depends(get_current_active_user)], instance_id: str
):
    try:
        instance = ec2.Instance(instance_id)
        if not user_in_resource_groups(current_user, instance):
            raise HTTPException(status_code=403)
        else:
            instance.start()
    except botocore.exceptions.ClientError as err:
        if "InvalidInstanceID" in err.response["Error"]["Code"]:
            raise HTTPException(status_code=404, detail="Invalid instance id")
        else:
            raise err


@app.post("/instances/{instance_id}/stop", status_code=204)
async def stop(
    current_user: Annotated[User, Depends(get_current_active_user)], instance_id: str
):
    try:
        instance = ec2.Instance(instance_id)
        if not user_in_resource_groups(current_user, instance):
            raise HTTPException(status_code=403)
        else:
            instance.stop()
    except botocore.exceptions.ClientError as err:
        if "InvalidInstanceID" in err.response["Error"]["Code"]:
            raise HTTPException(status_code=404, detail="Invalid instance id")
        else:
            raise err
