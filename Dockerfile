FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /mall_app
COPY requirements.txt /mall_app/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /mall_app/