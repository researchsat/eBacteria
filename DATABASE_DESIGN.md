# Database Design and Authentication Outline

This document outlines the conceptual database schema and authentication flow for the Microbial Analysis SaaS application. 
This is a design document; actual implementation will occur in later phases.

## 1. Pydantic Schemas

Pydantic models for data validation and serialization are defined in `app/schemas/data_models.py`. These include:
- `UserCreate`, `UserRead` for user management.
- `Token`, `TokenData` for authentication.
- `ImageMetadataCreate`, `ImageMetadataRead` for tracking uploaded images.
- `AnalysisResultBase`, `AnalysisResultCreate`, `AnalysisResultRead` for storing analysis outputs. (Note: `AnalysisResultBase` and its derivatives now include an optional `confidence_score` field).

## 2. Conceptual Database Tables

We plan to use a relational database (e.g., PostgreSQL or SQLite for initial development). The main tables would be:

### `users` Table
- `id` (Primary Key, Integer, Auto-incrementing)
- `email` (String, Unique, Indexed)
- `hashed_password` (String)
- `is_active` (Boolean, Default: True)
- `created_at` (Timestamp, Default: Current Time)

### `images` Table (stores metadata about images)
- `id` (Primary Key, Integer, Auto-incrementing)
- `uploader_id` (Foreign Key to `users.id`, Integer)
- `filename` (String)
- `uploaded_at` (Timestamp, Default: Current Time)
- `content_type` (String, Optional, e.g., "image/png")
- `size_bytes` (Integer, Optional)
- `storage_path` (String, e.g., path in a cloud storage bucket or local filesystem) 
  *(Note: Actual image files might be stored in a dedicated file/blob storage, not directly in the DB).*

### `analysis_results` Table
- `id` (Primary Key, Integer, Auto-incrementing)
- `image_id` (Foreign Key to `images.id`, Integer)
- `user_id` (Foreign Key to `users.id`, Integer, to know who ran the analysis)
- `analysis_type` (String, e.g., "colony_count", "microbial_identification", "growth_monitoring")
- `ran_at` (Timestamp, Default: Current Time)
- `result_data` (JSONB or Text, to store the actual analysis output, e.g., `{"count": 150}` or `{"species": "E. coli"}`)
- `confidence_score` (Float, Optional, e.g., 0.0 to 1.0, representing the AI model's confidence in the primary result like identification or classification)
- `model_version` (String, Optional, to track which AI model version produced the result)
- `parameters_used` (JSONB or Text, Optional, to store parameters used for the analysis)

### Relationships
- One `User` can upload many `Images`.
- One `Image` can have many `AnalysisResults` (e.g., same image analyzed with different models or parameters).
- One `User` can perform many `AnalysisResults`.

## 3. Authentication Flow (Conceptual)

We will use FastAPI's security utilities, likely based on OAuth2 with JWT (JSON Web Tokens).

1.  **Token Endpoint:**
    - A `/token` endpoint (e.g., implemented with `OAuth2PasswordRequestForm`) will accept a username (email) and password.
    - It will verify credentials against the `users` table.
    - If valid, it generates a JWT access token and returns it.

2.  **User Registration:**
    - A `/users/register` endpoint will accept user details (e.g., via `UserCreate` schema).
    - It will hash the password and store the new user in the `users` table.

3.  **Protected Endpoints:**
    - Most API endpoints (especially those for uploading data and triggering analysis) will be protected.
    - We'll use FastAPI's dependency injection with `OAuth2PasswordBearer`.
    - A dependency (e.g., `get_current_active_user`) will:
        - Extract the token from the `Authorization` header.
        - Decode and validate the JWT.
        - Fetch the user from the database based on token data (e.g., user ID or email).
        - Return the user object, making it available in the endpoint function.
        - Raise an `HTTPException` if the token is invalid or the user is not active.

4.  **Password Hashing:**
    - Passwords will be hashed using a strong algorithm (e.g., bcrypt or Argon2) via libraries like `passlib`.

## 4. Future Considerations
- Role-based access control (RBAC).
- API key authentication for external services.
- Refresh tokens.
