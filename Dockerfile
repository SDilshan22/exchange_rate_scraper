FROM python:3.12-slim

# Ensure output is not buffered
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install any required OS packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copy the summarized requirements file into the container
COPY requirements.txt .

# Upgrade pip and install the Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy your project files into the container
COPY . .

# Set the container's startup command to run the bash script
CMD ["/bin/bash"]
