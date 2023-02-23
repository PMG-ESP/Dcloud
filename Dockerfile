FROM python:3.10.10

RUN apt update
RUN apt install -y python3-pip

RUN apt install -y git
RUN git clone https://github.com/PMG-ESP/Dcloud.git

RUN pip install -r requirements.txt

CMD bash