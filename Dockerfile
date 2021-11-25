FROM devhub-docker.cisco.com/iox-docker/ir1101/base-rootfs:latest
RUN opkg update && opkg install python-pip 
RUN python -m pip install bottle
RUN opkg remove python-pip && opkg clean
EXPOSE 8010
COPY iox-ping-app.py /iox-ping-app.py
COPY iox-ping-app.sh /iox-ping-app.sh
RUN chmod 777 /iox-ping-app.sh
RUN ln -s /iox-ping-app.sh /etc/rc5.d/S50iox-ping-app.sh
CMD ["/iox-ping-app.sh"]
