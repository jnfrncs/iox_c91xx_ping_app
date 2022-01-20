FROM devhub-docker.cisco.com/iox-docker/ir1101/base-rootfs:latest
RUN opkg update && opkg install python-pip 
RUN python -m pip install bottle
RUN opkg remove python-pip && opkg clean
EXPOSE 8010
COPY iox_ping_app.py /usr/bin/iox_ping_app.py
COPY iox_ping_app.sh /usr/bin/iox_ping_app.sh
RUN chmod 777 /usr/bin/iox_ping_app.sh
