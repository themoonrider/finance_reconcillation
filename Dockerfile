FROM python:3.9-slim

# Set workdir
WORKDIR /app
# Copy local code to the container image
COPY . .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Generate db for 1000 users and 1000000 transactions and generate reports
RUN chmod +x /app/scripts.sh
ENTRYPOINT [ "/app/scripts.sh" ]