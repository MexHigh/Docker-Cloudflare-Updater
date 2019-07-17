FROM python:3.7.4-alpine3.10

WORKDIR /app/cf

# Copy the current directory contents into the container at /app
COPY . /app/cf/

# Install dependencies
RUN pip3 install cloudflare && \
    apk add --no-cache build-base curl python3-dev py-psutil

# Define environment variable
ENV FRITZBOX_ADDRESS=fritz.box
ENV CF_EMAIL=None
ENV CF_TOKEN=None
ENV ZONES_TO_UPDATE=None
ENV HOSTS_TO_IGNORE=None

HEALTHCHECK --start-period=5s \
  CMD ["python3", "healthcheck.py"]

# Run app.py when the container launches
CMD ["python3", "cfupdater.py"]
