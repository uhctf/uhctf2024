FROM python:3.12-alpine3.19
WORKDIR /app
COPY server.py requirements.txt tetris ./
RUN apk add -U git wget musl build-base
RUN pip install -r requirements.txt
ENV PORT=53
EXPOSE 53
CMD [ "/app/server.py" ]
