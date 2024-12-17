# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Add a non-root user
#RUN useradd -m appuser
#USER appuser

# Set the working directory in the container
WORKDIR /thingy91-api-brown

#RUN chown -R appuser:appuser /thingy91-api-brown

#USER appuser

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/thingy91-api-brown

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "run.py"]