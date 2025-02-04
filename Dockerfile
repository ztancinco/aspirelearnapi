FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies, including PostgreSQL client
RUN apt-get update \
    && apt-get install -y \
    build-essential \
    libpq-dev \
    pkg-config \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install linting tools
RUN pip install pylint autopep8 black ruff

# Copy application files
COPY . .

# Set Django settings module environment variable
ENV DJANGO_SETTINGS_MODULE=app.settings

# Run linting and auto-fixing (optional during build)
RUN pylint app || echo "Pylint completed with warnings/errors"
RUN autopep8 --in-place --recursive app
RUN black app
RUN ruff check app --fix

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]
