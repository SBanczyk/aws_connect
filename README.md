# aws_connect
Function that connects user to AWS server and performs one of three actions using FastAPI: start server, stop server or check current server state.
Database for authorization is PostgreSQL. Password is hashed using `CryptContext(schemes=["bcrypt"], deprecated="auto").hash()` method.

Following environmental variables must be set in `.env` file: 
- SECRET_KEY
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- REGION_NAME
- DB_IP
- DB_NAME
- DB_USER
- DB_PWD
