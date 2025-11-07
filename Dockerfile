FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY src/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY src/ .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bookstore.wsgi:application"]