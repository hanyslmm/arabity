FROM alpine:3.8

MAINTAINER hany salama <hanyslmm@gmail.com>

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache


# Install all app dependencies

RUN pip3 install Flask

RUN pip3 install Flask-SQLALchemy

RUN pip3 install oauth2client

RUN pip3 install httplib2

RUN pip3 install requests 

RUN python3 database_setup.py

# Bundle app source

COPY project.py /src/project.py
COPY database_setup.py /src/database_setup.py
COPY templates /src/templates
CMD ["python3", "/src/database_setup.py"]

