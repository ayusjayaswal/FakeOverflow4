# FakeOverflow's Fourth Rewrite
This project is supposed to be a standard template for building three-layer architecture CRUD applications, designed to be easily adaptable and deployable. It uses FastAPI for the server, Next.js for the client, and PostgreSQL with Redis for the database layer, providing a robust foundation for discussion-based or similar web applications. Other Stacks like those in Go and Node will also be added in the future this should arrive at different branches of the project. If you find this project useful you might want to drop a star to improve the project visibility :D

## Purpose
The primary purpose of this project is to provide a reusable, modular template for developing CRUD applications with a three-layer architecture (client, server, database). Its design prioritizes flexibility, allowing anyone to mold it to specific needs by modifying schemas, API endpoints, or UI components. The use of Docker and standardized tools ensures straightforward deployment across environments.

## Project Structure
The project is organized into two main directories: `app` for server-side code and `client` for client-side code. The server includes modules for API endpoints (`api`), business logic (`core`), database operations (`crud`), data models (`models`), data schemas (`schemas`), and utilities (`utils`). The client contains components, hooks, pages, and styles, following Next.js conventions. Configuration files like `docker-compose.yml`, `Dockerfile`, and `init.sql` streamline deployment and database setup.

## System Design Principles

The application follows a three-layer architecture: client layer, server layer, and database layer. The client layer, built with Next.js, handles user interfaces and client-side logic. The server layer, powered by FastAPI, manages business logic and API request processing. The database layer, using PostgreSQL for persistent storage and Redis for caching, ensures efficient data handling. This separation enhances modularity, scalability, and maintainability, making the template adaptable for various CRUD applications.

## Optimization

FastAPI’s asynchronous capabilities reduce latency in request handling, optimizing server performance. Redis caching minimizes database queries, improving response times. Docker containers isolate services for consistent environments and efficient resource use. The `docker-compose.yml` orchestrates services with health checks and dependency management, simplifying deployment. Persistent volumes for PostgreSQL and Redis balance data durability and performance.

## Type Safety

Pydantic, integrated with FastAPI, enforces type safety through strict data validation and serialization. Schemas in the `schemas` directory define robust data models, catching type errors early and ensuring reliable data exchange between client and server. This reduces bugs and supports customization by allowing developers to modify schemas for specific use cases.

## Adminer Usage

Adminer, a lightweight database management tool, is included for interacting with the PostgreSQL database. Accessible at `http://localhost:8080`, it enables SQL query execution, schema inspection, and data management. Adminer simplifies database debugging during development, making it easier to adapt the database layer to project-specific needs. Restrict Adminer access in production for security.

## Setup and Running

Ensure Docker and Docker Compose are installed. Clone the repository, navigate to the project root, and run:

```bash
docker-compose up --build
```

This builds and starts all services. The server runs on `http://localhost:8000`, the client on `http://localhost:3000`, and Adminer on `http://localhost:8080`. The database is initialized with `init.sql` on startup, providing a customizable starting point for database structures.
If you wish to refer the API Documentation this is available at `http://localhost:8000/docs`.

## Services

- **Server**: FastAPI application for API requests, running on port 8000.
- **Client**: Next.js application for the user interface, running on port 3000.
- **Database**: PostgreSQL for persistent storage on port 5432, and Redis for caching on port 6379.
- **Adminer**: Web-based database management tool, running on port 8080.

## Dependencies

Server dependencies are listed in `requirements.txt`. Client dependencies are in `client/package.json`. Both are installed automatically during Docker builds, ensuring consistent setups across deployments.

## Environment Variables

- **Server**: Configure `DATABASE_URL`, `REDIS_URL`, and `SECRET_KEY` in `docker-compose.yml`. Update `SECRET_KEY` for production.
- **Client**: Set `NEXT_PUBLIC_API_URL` to the server API endpoint (defaults to `http://localhost:8000`).

## Customization and Development

The template is designed for easy adaptation. Modify `schemas` and `models` in the server to adjust data structures, update `api` for custom endpoints, or extend `crud` for specific database operations. On the client, customize components, pages, or hooks to tailor the UI. Live updates are supported via volume mounts in `app` and `client` directories. For local client development outside Docker, run `npm run dev` in the `client` directory.

## Deployment

The Docker-based setup ensures portability across environments. Update environment variables in `docker-compose.yml` for production, and use a reverse proxy (e.g., Nginx) for load balancing if needed. The template’s modular structure and standardized tools (FastAPI, Next.js, PostgreSQL, Redis) simplify scaling and deployment for various CRUD applications.

## Security Notes

In production, update `SECRET_KEY` and the PostgreSQL password to secure values. Restrict Adminer access (port 8080) or disable it to prevent unauthorized database access. Ensure environment variables are securely managed, and avoid exposing sensitive ports publicly.
