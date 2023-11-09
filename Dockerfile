ARG IMAGE="python:3.10-slim"
FROM $IMAGE as builder

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required packages
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-deps sentence-transformers==2.2.2
RUN pip install --no-cache-dir -r requirements.txt

# Define the healthcheck command
HEALTHCHECK --interval=10s --timeout=5s --start-period=15s \ 
   CMD curl --fail localhost:8899/health || exit 1

# Expose port 8899 for the application to listen on
EXPOSE 8899

# Run the application
CMD ["python", "server.py"]