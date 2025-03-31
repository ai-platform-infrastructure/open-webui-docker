ARG UID_GID="35002:35002"

FROM apache/tika:3.1.0.0-full

USER root

# Add support for danish language in OCR.
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive \
	apt-get install -qy \
	tesseract-ocr-dan \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

 USER $UID_GID