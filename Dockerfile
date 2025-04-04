# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Command to run the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
