FROM python:3.12-alpine3.18
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
WORKDIR /charityAuctionProject
RUN apk update && \
    apk add gcc && \
    apk add libffi-dev && \
    apk add musl-dev && \
    apk add --no-cache bash && \
    apk add --no-cache postgresql-libs && \
    apk add postgresql-dev gcc python3-dev musl-dev && \
    pip install pip-tools
COPY . .
RUN pip-compile requirements/requirements.ini
RUN pip-sync requirements/requirements.txt
RUN chmod +x entrypoint.sh
RUN chmod -R 755 static
RUN chmod -R 755 staticfiles