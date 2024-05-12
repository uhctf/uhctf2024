FROM nginx:1.25.5-alpine
COPY site.tar.xz /archive.tar.xz
RUN apk add --no-cache tar xz
RUN cd /usr/share/nginx/html && tar -xf /archive.tar.xz
RUN rm /archive.tar.xz

