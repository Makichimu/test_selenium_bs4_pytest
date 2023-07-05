# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /home

# Copy the current directory contents into the container at /app
COPY . /home

# Install Firefox and GeckoDriver
RUN apt-get update && \
    apt-get install -y --no-install-recommends firefox-esr && \
    wget -qO- https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar xvz -C /usr/local/bin

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run the tests when the container launches
CMD ["pytest", "--junitxml=/results/test-results.xml"]
