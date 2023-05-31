FROM python:3.11-slim

WORKDIR /pitest-app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app ./app

EXPOSE 8000
CMD [ "flask","--app","app.main","run","--host","0.0.0.0","--port","8000"]