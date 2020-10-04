# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Install prerequisites
RUN apt-get update && apt-get install -y \
curl
CMD /bin/bash

# Set the working directory to /
WORKDIR /

# Copy the current directory contents into the container at /
COPY . /

RUN apt-get update
RUN curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb




# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt



# Define environment variable
ENV NAME World

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["flask", "run", "-h", "0.0.0.0"]
