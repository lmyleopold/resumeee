FROM python:3.10-bookworm

WORKDIR /resumee
COPY . /resumee

RUN apt update && apt install libmariadb-dev
RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/sh", "run.sh"]