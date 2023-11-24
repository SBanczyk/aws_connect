import boto3
import configparser
import botocore.exceptions
from fastapi import FastAPI, HTTPException


app = FastAPI()
config = configparser.ConfigParser()
config.read("config.ini")
try:
    session = boto3.Session(
        aws_access_key_id=config['CREDENTIALS']['aws_access_key_id'],
        aws_secret_access_key=config['CREDENTIALS']['aws_secret_access_key'],
        region_name=config['CREDENTIALS']['region_name']
    )
    ec2 = session.resource('ec2')
except KeyError:
    print(f"config.ini does not exist, is of incorrect type, has incorrect structure or contains "
          f"incorrect credential names")


@app.get("/instances/{instance_id}/status")
async def status(instance_id: str):
    try:
        instance = ec2.Instance(instance_id)
        return instance.state
    except botocore.exceptions.ClientError as err:
        if err.response["Error"]["Code"] == "InvalidInstanceID.Malformed":
            raise HTTPException(status_code=404, detail="Incorrect instance id")
        else:
            return err


@app.get("/instances/{instance_id}/start")
async def start(instance_id: str):
    try:
        instance = ec2.Instance(instance_id)
        instance.start()
        raise HTTPException(status_code=204)
    except botocore.exceptions.ClientError as err:
        if err.response["Error"]["Code"] == "InvalidInstanceID.Malformed":
            raise HTTPException(status_code=404, detail="Incorrect instance id")
        else:
            return err


@app.get("/instances/{instance_id}/stop")
async def stop(instance_id: str):
    try:
        instance = ec2.Instance(instance_id)
        instance.stop()
        raise HTTPException(status_code=204)
    except botocore.exceptions.ClientError as err:
        if err.response["Error"]["Code"] == "InvalidInstanceID.Malformed":
            raise HTTPException(status_code=404, detail="Incorrect instance id")
        else:
            return err
