FROM python:3.9-slim

# Set workdir
WORKDIR /app
# Copy local code to the container image
COPY . .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Generate db for 1000 users and 1000000 transactions and generate reports
RUN python generate_db.py 100 10000

# Generated reports
CMD ["python", "reconcillation_tl.py"]