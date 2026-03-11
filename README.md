# rest-api-application

---

# PostgreSQL Database Docker Setup

This project uses **Docker Compose** to run a PostgreSQL database inside a Docker container. The configuration allows you to easily start a PostgreSQL instance with predefined environment variables and persistent storage.

---

## Overview

The `postgres.yml` file defines a service that runs a PostgreSQL database container.

Main features:

* Uses an official PostgreSQL Docker image
* Configurable version of PostgreSQL
* Environment-based configuration
* Automatic restart of the container
* Persistent database storage using Docker volumes
* Port mapping between host and container

---

## File: postgres.yml Explanation

## Services

### PostgreSQL Database Service

```yaml
services:
  postgres_db:
```

This defines a service named **postgres_db**, which runs the PostgreSQL database container.

---

### PostgreSQL Image

```yaml
image: postgres:${POSTGRES_VERSION}
```

This tells Docker to pull the **official PostgreSQL image** from Docker Hub.

`${POSTGRES_VERSION}` allows you to specify the PostgreSQL version using environment variables.

Example:

```
POSTGRES_VERSION=15
```

---

### Container Name

```yaml
container_name: db
```

This assigns a fixed name **db** to the running container.

This makes it easier to reference the container when running Docker commands.

Example:

```
docker logs db
```

---

### Environment Variables

```yaml
environment:
  POSTGRES_USER: ${POSTGRES_USER}
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
  POSTGRES_DB: ${POSTGRES_DB}
```

These variables configure the PostgreSQL database:

| Variable          | Description                         |
| ----------------- | ----------------------------------- |
| POSTGRES_USER     | Database username                   |
| POSTGRES_PASSWORD | Database password                   |
| POSTGRES_DB       | Default database created at startup |

Values are read from environment variables (usually from a `.env` file).

Example `.env` file:

```
POSTGRES_VERSION=15
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret
POSTGRES_DB=mydatabase
POSTGRES_PORT=5432
```

---

### Port Mapping

```yaml
ports:
  - "${POSTGRES_PORT}:5432"
```

This maps the **container's PostgreSQL port (5432)** to a port on your host machine.

Example:

```
5432:5432
```

This allows applications on your machine to connect to the database.

Example connection:

```
localhost:5432
```

---

### Persistent Storage (Volumes)

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

This stores PostgreSQL data in a **Docker named volume** called `postgres_data`.

Benefits:

* Data persists even if the container stops or is removed
* Prevents database data loss

---

## Volumes Section

```yaml
volumes:
  postgres_data:
```

This defines the named volume used by PostgreSQL to store its data.

Docker automatically manages this volume.

---

## How to Run the Project

### 1. Create `.env` file

Create a `.env` file in the same directory:

```
POSTGRES_VERSION=15
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret
POSTGRES_DB=mydatabase
POSTGRES_PORT=5432
```

---

### 2. Start the Container

Run:

```bash
docker compose -f postgres.yaml up -d
```

This will:

* Pull the PostgreSQL image
* Create the container
* Start the database

---

### 3. Check Running Containers

```bash
docker ps
```

---

### 4. Stop the Container

```bash
docker compose down
```

---

## Database Connection Details

Example connection parameters:

| Parameter | Value      |
| --------- | ---------- |
| Host      | localhost  |
| Port      | 5432       |
| Username  | admin      |
| Password  | secret     |
| Database  | mydatabase |

---