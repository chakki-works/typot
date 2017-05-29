FROM python:3.4.5

RUN apt-get update
RUN apt-get install -y enchant

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -qr /tmp/requirements.txt

ADD ./typot /opt/typot/
WORKDIR /opt/typot

# Expose is NOT supported by Heroku
# EXPOSE 8000

CMD hug -p $PORT -f /opt/typot/api.py 
