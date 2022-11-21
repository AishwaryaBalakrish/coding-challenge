# Dockerfile

FROM python:latest

WORKDIR /ryanair_project

COPY requirements.txt /ryanair_project

RUN apt-get update

RUN apt-get install -y chromium

RUN pip install pip --upgrade &&  pip install -r requirements.txt

COPY *.py /ryanair_project
COPY ./web_apis/*.py /ryanair_project/web_apis/

CMD [ "pytest", "./test_cases.py", "--html=report.html"]