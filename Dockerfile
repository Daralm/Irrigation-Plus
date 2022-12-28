FROM python:3

WORKDIR /app

ENV TZ="Australia/Melbourne"

COPY . /app

RUN pip install -r dependencies/requirements.txt

CMD ["python", "src/main.py", "config/config.yaml"]
