FROM alpine:3.8

MAINTAINER hany salama <hanyslmm@gmail.com>

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache


 
WORKDIR /code/

# Add requirements and install dependencies 
ADD ./files/requirements.txt /code/
RUN pip install -r ./requirements.txt

WORKDIR /code/src
COPY database_setup_arabity.py .

# Bundle app source
RUN mkdir templates
RUN mkdir static
COPY project.py .
COPY templates ./templates
COPY static ./static
COPY client_secrets.json .
COPY arabity.db .
