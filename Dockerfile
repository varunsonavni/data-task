# Use a more specific base image tag for better reproducibility
FROM python:3.9-slim-bullseye

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy only the required files
# This helps with layer caching and reduces image size
COPY fixed_width_parser.py spec.json ./

# Set proper ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set default command using exec form
ENTRYPOINT ["python", "fixed_width_parser.py"]

