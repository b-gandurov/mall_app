FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /mall_app
COPY requiremnts.txt /mall_app/
RUN pip install -r requiremnts.txt
COPY . /mall_app/