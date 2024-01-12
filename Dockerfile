FROM python:3.11

WORKDIR /usr/src/app

RUN curl -sSL https://install.python-poetry.org | python3 -
COPY poetry.lock ./
COPY pyproject.toml ./
ENV PATH=/root/.local/bin:$PATH
RUN poetry install

COPY aws_connect.py ./

EXPOSE 8000

CMD [ "poetry", "run", "uvicorn", "aws_connect:app", "--host", "0.0.0.0", "--port", "8000"]
