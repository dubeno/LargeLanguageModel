# Use an official Python runtime as a parent image.
# Using a slim image for a smaller final size and reduced attack surface.
FROM python:3.9-slim

# Set the maintainer label for metadata.
LABEL maintainer="fernandodorado.rueda@ingka.com"

# Set environment variables for a consistent build behavior.
# Disabling the buffer helps to log messages synchronously.
ENV PYTHONUNBUFFERED=1

# Set a working directory inside the container to store all our project files.
WORKDIR /app

# First, copy the requirements file to leverage Docker's cache for dependencies.
# By doing this first, changes to the code will not invalidate the cached dependencies.
COPY requirements.txt requirements.txt

# Install the required packages listed in the requirements file.
# It's a good practice to include the --no-cache-dir flag to prevent the caching of dependencies
# that aren't necessary for executing the application.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code and model files into the image.
COPY DockerModel.py DockerModel.py
COPY models/    models/

# Expose ports that the application will run on.
# Port 5000 for GRPC
# Port 9000 for REST
EXPOSE 5000 9000

# Set environment variables used by the application.
ENV MODEL_NAME DockerModel
ENV SERVICE_TYPE MODELdocker

# Change the owner of the directory to user 8888 for security purposes.
# It can prevent unauthorised write access by the application itself.
# Make sure to run the application as this non-root user later if applicable.
RUN chown -R 8888 /app

# Use the exec form of CMD so that the application you run will receive UNIX signals.
# This is helpful for graceful shutdown.
# Here we're using seldon-core-microservice to serve the model.
CMD exec seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE