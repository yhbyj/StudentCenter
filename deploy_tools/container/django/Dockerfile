FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
  && apk add --update --no-cache postgresql-client jpeg-dev \
  && apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev libffi-dev linux-headers postgresql-dev musl-dev zlib zlib-dev git \
  && git clone https://github.com/yhbyj/StudentCenter.git \
  && pip install --no-chache-dir -r StudentCenter/requirements.txt -i https://mirrors.aliyun.com/pypi/simple \
  && apk del .tmp-build-deps \
  && adduser -D user

USER user
