# FastAPI Authentication Starter

This is a basic FastAPI starter template with authentication implemented using JWT (JSON Web Tokens) and asyncpg for database interaction with PostgreSQL.

## Features

*   **User Registration:**  Allows users to create accounts with email, username, and password.
*   **User Login:** Authenticates users using email and password and generates JWT tokens.
*   **JWT Authentication:** Protects routes by requiring a valid JWT token in the `Authorization` header.
*   **Password Hashing:** Uses `passlib` for secure password hashing with bcrypt.
*   **Async Database Connectivity:** Utilizes `asyncpg` for asynchronous database operations.
*   **Environment Variable Configuration:** Uses `pydantic-settings` to manage configuration through environment variables.
*   **CORS Support:**  Configured for Cross-Origin Resource Sharing.

## Prerequisites

*   Python 3.7+
*   PostgreSQL Database

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/KrishChordiya/fastapi-auth-starter.git
    cd fastapi-auth-starter
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**

    Create a `.env` file in the root directory and set the following environment variables:

    ```
    DATABASE_URL=<your_postgresql_connection_string>
    SECRET_KEY=<your_secret_key>  # A random, long, and secret string
    ACCESS_TOKEN_EXPIRE_MINUTES=<int> # Time for token expiry
    ```

5.  **Database Setup:**

    Create a PostgreSQL database and run the following SQL script to create the `users` table:

    ```sql
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        username VARCHAR(255) NOT NULL,
        hashed_password VARCHAR(255) NOT NULL
    );
    ```

## Running the Application

```bash
uvicorn app.main:app --reload
```

This will start the FastAPI application with hot reloading enabled.

## API Endpoints

*   **POST `/auth/signin`:**  Registers a new user.  Requires `email`, `username`, and `password` in the request body.
*   **POST `/auth/login`:** Logs in an existing user. Requires `email` and `password` in the request body.  Returns an `access_token` (JWT).
*   **GET `/protected`:** Example protected route.  Requires a valid JWT token in the `Authorization` header.

## Authentication

To access protected routes, you need to include the `Authorization` header in your request with the following format:

```
Authorization: Bearer <access_token>
```

Replace `<access_token>` with the token you received after logging in.

## Future Enhancements

*   **Password Reset:** Implement password reset functionality.
*   **User Profile:** Add endpoints for managing user profiles.
*   **Token Refresh:** Implement token refresh mechanism for better security.
*   **Tests:** Add unit and integration tests.
*   **Role-Based Access Control (RBAC):** Implement RBAC for finer-grained access control.
*   **Rate Limiting:** Implement rate limiting to protect against abuse.
