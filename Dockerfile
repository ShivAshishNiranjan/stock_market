FROM python:3.8.0-slim

ENV SRC_PATH /src

RUN apt-get update && \
    apt-get -y install git procps curl vim net-tools build-essential \
    libpq-dev

COPY requirement.txt .

RUN python -m pip install pip==19.2.1  && \
pip install -r requirement.txt

RUN mkdir ${SRC_PATH}
COPY . ${SRC_PATH}
WORKDIR ${SRC_PATH}
ENV PYTHONPATH "${PYTHONPATH}:${SRC_PATH}"
ENTRYPOINT ["python3",  "src/main.py"]




