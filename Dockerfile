FROM python:3.11

WORKDIR /home/app

COPY model /home/app/model
COPY templates /home/app/templates
COPY requirements.txt /home/app/requirements.txt
RUN mkdir -p static/uploads
RUN pip install -r requirements.txt

CMD [ "python3", "model/app.py" ]