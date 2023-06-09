FROM python:3.11
WORKDIR /app
RUN pip3 install --upgrade setuptools
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN chmod 755 .
COPY . .
