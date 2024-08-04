# Use the official Python image.
FROM python:3.9

# Set the working directory in the container.
WORKDIR /app

# Copy the dependencies file to the working directory.
COPY requirements.txt .

# Install any dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory.
COPY . .

# Build the frontend
RUN cd app/frontend && npm install && npm run build

# Command to run the Alembic migrations and start the FastAPI server.
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port ${WEB_PORT}"]
