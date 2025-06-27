# Use official Python image
FROM python:3.10.6-slim

# Set working directory inside the container
WORKDIR /app

# Copy project files to container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port (default 5000)
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
