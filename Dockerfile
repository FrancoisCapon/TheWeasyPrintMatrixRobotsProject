FROM debian:bullseye-slim

# https://stackoverflow.com/questions/27273412/cannot-install-packages-inside-docker-ubuntu-image
RUN apt-get update -yq

# https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#linux
# https://packages.debian.org/bullseye/pango1.0-tools
RUN apt-get install -yq python3 pango1.0-tools

# https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#debian-11
RUN apt-get install -yq python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0
RUN pip install weasyprint==62.1

# https://github.com/sass/dart-sass#standalone
RUN apt-get install wget -yq
WORKDIR /tmp
RUN wget https://github.com/sass/dart-sass/releases/download/1.49.9/dart-sass-1.49.9-linux-x64.tar.gz
RUN tar --strip-components 1 -xzzf dart-sass-1.49.9-linux-x64.tar.gz -C /usr/local/bin dart-sass/sass
RUN rm dart-sass-1.49.9-linux-x64.tar.gz

RUN mkdir /project
WORKDIR /project

