import sys
import boto3
import configparser
import botocore.exceptions


def aws_connect(config_file_path: str, action: str):
    config = configparser.ConfigParser()
    config.read(config_file_path)
    try:
        session = boto3.Session(
            aws_access_key_id=config['CREDENTIALS']['aws_access_key_id'],
            aws_secret_access_key=config['CREDENTIALS']['aws_secret_access_key'],
            region_name=config['CREDENTIALS']['region_name']
        )
        ec2 = session.resource('ec2')
        instance = ec2.Instance(config['CREDENTIALS']['instance_id'])
    except KeyError:
        print(f"{config_file_path} does not exist, is of incorrect type, has incorrect structure or contains "
              f"incorrect credential names")
        return
    try:
        if action == "start":
            instance.start()
        elif action == "stop":
            instance.stop()
        elif action == "state":
            print(instance.state)
        else:
            print("Available aruments: start, stop, state")
    except botocore.exceptions.ClientError as err:
        print(err)
        return


def main():
    if len(sys.argv) != 3:
        print("Usage: ./aws_connect <config_file_path> <action>")
    else:
        aws_connect(sys.argv[1], sys.argv[2])
    return 0


if __name__ == '__main__':
    sys.exit(main())
