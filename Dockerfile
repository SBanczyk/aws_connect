FROM python:3.11

WORKDIR /usr/src/app

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN curl -OL https://github.com/protocolbuffers/protobuf/releases/download/v25.0-rc1/protoc-25.0-rc-1-linux-x86_64.zip
RUN unzip protoc-25.0-rc-1-linux-x86_64.zip -d protoc
RUN mv protoc/bin/* /usr/local/bin/
RUN mv protoc/include/* /usr/local/include/
RUN chmod +x /usr/local/bin/protoc
COPY poetry.lock ./
COPY pyproject.toml ./
COPY aws_connect_log.proto ./
RUN protoc -I=. --python_out=. ./aws_connect_log.proto
ENV PATH=/root/.local/bin:$PATH
RUN poetry install

COPY aws_connect.py ./

EXPOSE 8000

CMD [ "poetry", "run", "uvicorn", "aws_connect:app", "--host", "0.0.0.0", "--port", "8000"]
