# AspireLearn API

AspireLearn API is a backend application designed for managing courses, lessons, quizzes, and instructors

## Features

- **Course Management**: Create, update, delete, and view courses.
- **Lesson Management**: Associate lessons with courses, manage their order, and include content and videos.
- **Quiz Management**: Add quizzes to courses or lessons, manage questions, and track results.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ztancinco/aspirelearnapi.git
   cd aspirelearnapi
   ```
2. If using Docker, build and run the application using the following command:
   ```bash
   docker-compose up --build -d
   ```

### Environment Variables

```bash
DJANGO_SECRET_KEY=secret-key
POSTGRES_DB=your-db
POSTGRES_USER=db-user
POSTGRES_PASSWORD=db-password
POSTGRES_HOST=db
POSTGRES_PORT=db-port
DEBUG=True/False
DJANGO_SUPERUSER_USERNAME=django-admin
DJANGO_SUPERUSER_PASSWORD=django-admin-password
DJANGO_SUPERUSER_EMAIL=django-admin-email
DJANGO_API_VERSION=api-version
```
