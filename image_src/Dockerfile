FROM python:3.7.4-alpine3.10

WORKDIR /app/cf

# Copy the current directory contents into the container at /app
COPY . /app/cf/

# Install dependencies
RUN pip3 install cloudflare && \
    apk add --no-cache bash curl

# Define environment variable
ENV FRITZBOX_ADDRESS=fritz.box \
    CF_EMAIL=None \
    CF_TOKEN=None \
    ZONES_TO_UPDATE=None \
    HOSTS_TO_IGNORE=None

HEALTHCHECK NONE

# Run app.py when the container launches
CMD ["python3", "cfupdater.py"]
