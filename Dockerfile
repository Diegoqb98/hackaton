# Step 1: Use an official Python runtime as a parent image
FROM python:3.12-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Install dependencies from requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the entire project folder into the container
COPY . .

# Step 5: Create the 'files' directory (if not exist) and set appropriate permissions
RUN mkdir -p /app/files && chmod -R 777 /app/files

# Step 6: Set environment variables from .env (if any)
COPY .env .env

# Step 7: Run the Python script
CMD ["python", "main.py"]
