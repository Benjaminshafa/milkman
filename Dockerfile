FROM python:3

 COPY main.py /

RUN pip install requests
RUN pip install xlwt
RUN pip install azure-storage

 CMD [ "python", "./main.py" ]