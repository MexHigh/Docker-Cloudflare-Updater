FROM alpine:3.7

LABEL maintainer="Leon Schmidt"

WORKDIR /app/cf

# Copy the current directory contents into the container at /app
COPY ./image_src/ /app/cf/

# Install dependencies
RUN apk add --no-cache bash python3 curl && \
    pip3 install --no-cache --upgrade pip setuptools wheel cloudflare

# Define environment variable
ENV FRITZBOX_ADDRESS=fritz.box \
    CF_EMAIL=None \
    CF_TOKEN=None \
    ZONES_TO_UPDATE=None \
    HOSTS_TO_IGNORE=None

# Run app.py when the container launches
CMD ["python3", "-u", "cfupdater.py"]
