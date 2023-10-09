FROM python:3.9-slim

# Set workdir
WORKDIR /app
# Copy local code to the container image
COPY . .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt


# Generate reports
CMD ["python", "reconcillation_tl.py"]