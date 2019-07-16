FROM python:3.7-slim-stretch

WORKDIR /app/cf

# Copy the current directory contents into the container at /app
COPY . /app/cf/

# Install dependencies
RUN apt update && apt install curl -y && pip3 install cloudflare

# Define environment variable
ENV FRITZBOX_ADDRESS=fritz.box
ENV CF_EMAIL=None
ENV CF_TOKEN=None
ENV ZONES_TO_UPDATE=None
ENV HOSTS_TO_IGNORE=None

# Run app.py when the container launches
CMD ["python3", "cfupdater.py"]
