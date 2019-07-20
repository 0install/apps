FROM debian:10
RUN apt-get update && apt-get install -y 0install-core python-gobject wget --no-install-recommends
RUN 0install add 0repo http://0install.net/tools/0repo.xml
RUN mkdir -p /repo/incoming /repo/public
WORKDIR /repo
ADD ci.sh 0repo-config.py /repo/
