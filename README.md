# aws_connect
Function that connects user to aws server and performs one of three actions: start server, stop server or check current server state.
It takes 2 arguments: path to the `.ini` file with all neccessery credentials and action to perform on the server.
All credentials in the `.ini` file must be in the section `[CREDENTIALS]`.  
Example: `python ./aws_connect <path to .ini file> <action>`