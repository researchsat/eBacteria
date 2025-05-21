# Scalability Design Document

This document outlines conceptual approaches to enhance the scalability of the Microbial Analysis SaaS application, focusing on asynchronous task processing for AI analyses and scalable image storage.

## 1. Asynchronous Task Processing for AI Analyses

**Problem:** AI model inference (especially for complex images or large datasets) can be time-consuming. Synchronous API requests for these tasks can lead to long wait times for users and potential request timeouts.

**Solution:** Implement an asynchronous task processing system using a distributed task queue like Celery with a message broker such as Redis or RabbitMQ.

**Conceptual Flow:**

1.  **Task Definition:**
    *   AI analysis functions (e.g., `run_colony_counting_model`, `run_identification_model`) will be defined as Celery tasks (e.g., decorated with `@celery_app.task`).
    *   These tasks will take necessary inputs (e.g., image ID, parameters) and perform the computation.
    *   Upon completion, they will store their results, potentially in the `analysis_results` database table, associating them with a task ID or image ID.

2.  **API Endpoints for Task Management:**
    *   **Initiate Analysis (e.g., `POST /api/v1/async/analyze/colony_count`):**
        *   Accepts image reference and parameters.
        *   Does *not* run the analysis immediately. Instead, it queues the corresponding Celery task (e.g., `run_colony_counting_model.delay(image_id, params)`).
        *   Returns an immediate response (e.g., HTTP 202 Accepted) including a `task_id`.
    *   **Check Task Status (e.g., `GET /api/v1/async/status/{task_id}`):**
        *   Allows the client to poll for the status of a task (e.g., PENDING, STARTED, SUCCESS, FAILURE).
        *   Celery provides mechanisms to query task states.
    *   **Retrieve Task Result (e.g., `GET /api/v1/async/result/{task_id}`):**
        *   If the task is successful, this endpoint retrieves the results. The results might be fetched from the database (linked via `task_id` or another identifier) or directly from Celery's result backend (if configured).
        *   This could also be combined with the status endpoint, returning the result if available.

3.  **Celery Worker(s):**
    *   One or more Celery worker processes run independently of the API server.
    *   These workers listen to the message queue for new tasks and execute them.
    *   Workers can be scaled horizontally (running more worker instances) to handle increased load.

4.  **Result Backend:**
    *   Celery needs a result backend (e.g., Redis, database) to store the state and results of tasks if they need to be retrieved later by clients.

**Frontend Integration:**

*   The frontend initiates an analysis and receives a `task_id`.
*   It then polls the status endpoint periodically.
*   UI updates reflect the task status (e.g., "Processing...", "Analysis Complete").
*   Once complete, the frontend fetches and displays the results.

## 2. Scalable Image Storage

**Problem:** Storing a large number of potentially large image files directly on the API server's filesystem is not scalable, makes deployments complex, and is risky for data durability.

**Solution:** Utilize cloud-based object storage services like Amazon S3, Google Cloud Storage (GCS), or Azure Blob Storage.

**Conceptual Changes:**

1.  **Image Upload Process:**
    *   **Direct Upload (Preferred for Scalability):**
        *   The client (frontend) can request a pre-signed URL from the backend API to upload the image directly to the cloud storage service.
        *   This offloads the bandwidth and processing from the API server.
        *   Upon successful upload to cloud storage, the client notifies the backend API with the image's URL/path in cloud storage and any other metadata.
    *   **Indirect Upload (Simpler but less scalable):**
        *   The client uploads the image to the API server.
        *   The API server then streams/uploads the image to the cloud storage service.

2.  **Storing Image References:**
    *   The `images` table in the database will not store the image blob itself. Instead, it will store a reference to the image in cloud storage (e.g., the object key/path or the full URL).
    *   The `ImageMetadata` Pydantic model and the `images` table's `storage_path` field (from `DATABASE_DESIGN.md`) would be used for this.

3.  **Image Access for AI Models:**
    *   When an AI model needs to process an image, the Celery task (or the API if synchronous) will:
        *   Retrieve the image's storage path/URL from the database.
        *   Download the image from cloud storage to a temporary location on the worker/server for processing.
        *   Alternatively, some AI services or libraries might be able to read directly from cloud storage URLs.

4.  **Serving Images (if needed for display):**
    *   If the application needs to display original or processed images, it can generate pre-signed URLs for client-side rendering, providing temporary, secure access directly from cloud storage.

**Benefits:**

*   **Durability & Availability:** Cloud storage services offer high durability and availability.
*   **Scalability:** Object storage scales virtually infinitely.
*   **Cost-Effectiveness:** Often more cost-effective for storage than block storage attached to servers.
*   **Decoupling:** Separates image storage concerns from the application logic.

This document provides a high-level overview. Detailed implementation would require choosing specific services, configuring SDKs, and adjusting security policies (e.g., IAM roles, bucket policies).
