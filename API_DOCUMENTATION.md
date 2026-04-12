# PPT Generator API Documentation

## Overview

The PPT Generator API provides AI-powered PowerPoint presentation generation using Claude. It allows you to create presentations from natural-language prompts, upload and transform existing presentations into reusable templates, and manage stored templates.

**Base URL:** `http://localhost:8000`  
**API Prefix:** `/api/v1`  
**Interactive Docs:** `http://localhost:8000/docs` (Swagger UI)  
**ReDoc:** `http://localhost:8000/redoc`

---

## Authentication

The API itself does not require authentication headers from clients. However, the server must be configured with a valid `ANTHROPIC_API_KEY` environment variable to use AI generation features.

---

## Endpoints

### Health Check

#### `GET /health`

Returns the current health status of the server.

**Request**

```
GET /health
```

**Response `200 OK`**

```json
{
  "status": "ok"
}
```

---

### Generate Presentation

#### `POST /api/v1/generate`

Generate a new PowerPoint presentation from a natural-language text prompt using Claude AI.

**Request Headers**

| Header         | Value              |
|----------------|--------------------|
| `Content-Type` | `application/json` |

**Request Body**

| Field         | Type    | Required | Default | Description                                               |
|---------------|---------|----------|---------|-----------------------------------------------------------|
| `prompt`      | string  | ✅ Yes   | —       | Text prompt describing the presentation (min 10 chars).   |
| `template_id` | string  | ❌ No    | `null`  | ID of a saved template to apply.                          |
| `slide_count` | integer | ❌ No    | `8`     | Number of slides to generate (1–50).                      |
| `theme`       | string  | ❌ No    | `null`  | Visual theme name (e.g. `"corporate"`, `"default"`).      |

**Example Request**

```json
{
  "prompt": "Create a 5-slide presentation about machine learning for beginners",
  "slide_count": 5,
  "theme": "corporate"
}
```

**Response `201 Created`**

```json
{
  "id": "d3a4b5c6-1234-5678-abcd-ef1234567890",
  "filename": "presentation_d3a4b5c6.pptx",
  "download_url": "/generated/presentation_d3a4b5c6.pptx",
  "slide_count": 5,
  "created_at": "2026-04-12T05:00:00",
  "prompt": "Create a 5-slide presentation about machine learning for beginners"
}
```

**Error Responses**

| Status | Description                              |
|--------|------------------------------------------|
| `422`  | Validation error (e.g. prompt too short) |
| `500`  | Internal server error / generation failed|

---

### Transform Presentation

#### `POST /api/v1/transform`

Upload an existing `.pptx` file and convert it into a reusable template stored in the database.

**Request**

This endpoint accepts `multipart/form-data`.

| Field         | Type   | Required | Description                                  |
|---------------|--------|----------|----------------------------------------------|
| `file`        | file   | ✅ Yes   | A `.pptx` file to transform into a template. |
| `name`        | string | ❌ No    | Name for the new template.                   |
| `description` | string | ❌ No    | Optional description of the template.        |

**Example Request (curl)**

```bash
curl -X POST http://localhost:8000/api/v1/transform \
  -F "file=@my_presentation.pptx" \
  -F "name=My Corporate Template" \
  -F "description=Blue corporate theme with logo"
```

**Response `201 Created`**

```json
{
  "id": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
  "name": "My Corporate Template",
  "description": "Blue corporate theme with logo",
  "theme": null,
  "slide_count": 10,
  "created_at": "2026-04-12T05:00:00"
}
```

**Error Responses**

| Status | Description                              |
|--------|------------------------------------------|
| `400`  | File is not a `.pptx` file               |
| `422`  | Validation error                         |
| `500`  | Internal server error / transform failed |

---

### Upload Template

#### `POST /api/v1/upload-template`

Upload a JSON file that defines a presentation template structure.

**Request**

This endpoint accepts `multipart/form-data`.

| Field  | Type | Required | Description                              |
|--------|------|----------|------------------------------------------|
| `file` | file | ✅ Yes   | A `.json` file defining a template.      |

**Example Template JSON**

```json
{
  "name": "Business Quarterly",
  "description": "Q-review style template",
  "theme": "corporate",
  "slides": [
    {
      "title": "Executive Summary",
      "layout": "title"
    },
    {
      "title": "Financial Results",
      "layout": "content"
    }
  ]
}
```

**Example Request (curl)**

```bash
curl -X POST http://localhost:8000/api/v1/upload-template \
  -F "file=@template.json"
```

**Response `201 Created`**

```json
{
  "id": "f1e2d3c4-b5a6-7890-abcd-ef1234567890",
  "name": "Business Quarterly",
  "description": "Q-review style template",
  "theme": "corporate",
  "slide_count": 2,
  "created_at": "2026-04-12T05:00:00"
}
```

**Error Responses**

| Status | Description                          |
|--------|--------------------------------------|
| `400`  | File is not a `.json` file           |
| `422`  | Validation error or invalid JSON     |
| `500`  | Internal server error                |

---

### List Templates

#### `GET /api/v1/templates`

Return all stored presentation templates.

**Request**

```
GET /api/v1/templates
```

**Response `200 OK`**

```json
{
  "templates": [
    {
      "id": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
      "name": "My Corporate Template",
      "description": "Blue corporate theme with logo",
      "theme": null,
      "slide_count": 10,
      "created_at": "2026-04-12T05:00:00"
    }
  ],
  "total": 1
}
```

---

### Get Presentation

#### `GET /api/v1/presentation/{presentation_id}`

Retrieve metadata and download link for a previously generated presentation.

**Path Parameters**

| Parameter         | Type   | Description                       |
|-------------------|--------|-----------------------------------|
| `presentation_id` | string | UUID of the generated presentation|

**Example Request**

```
GET /api/v1/presentation/d3a4b5c6-1234-5678-abcd-ef1234567890
```

**Response `200 OK`**

```json
{
  "id": "d3a4b5c6-1234-5678-abcd-ef1234567890",
  "filename": "presentation_d3a4b5c6.pptx",
  "download_url": "/generated/presentation_d3a4b5c6.pptx",
  "slide_count": 5,
  "created_at": "2026-04-12T05:00:00",
  "prompt": "Create a 5-slide presentation about machine learning for beginners"
}
```

**Error Responses**

| Status | Description                             |
|--------|-----------------------------------------|
| `404`  | Presentation with given ID not found    |

---

## Error Response Format

All error responses follow this format:

```json
{
  "detail": "Human-readable error message"
}
```

Validation errors (`422`) return a more detailed structure:

```json
{
  "detail": [
    {
      "loc": ["body", "prompt"],
      "msg": "String should have at least 10 characters",
      "type": "string_too_short"
    }
  ]
}
```

---

## Usage Examples

### curl

```bash
# Health check
curl http://localhost:8000/health

# Generate a presentation
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Introduction to Python programming for beginners", "slide_count": 6}'

# List all templates
curl http://localhost:8000/api/v1/templates

# Get a specific presentation
curl http://localhost:8000/api/v1/presentation/<presentation_id>

# Transform a PPTX into a template
curl -X POST http://localhost:8000/api/v1/transform \
  -F "file=@my_presentation.pptx" \
  -F "name=My Template"

# Upload a JSON template definition
curl -X POST http://localhost:8000/api/v1/upload-template \
  -F "file=@template.json"
```

### Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Generate a presentation
response = requests.post(f"{BASE_URL}/generate", json={
    "prompt": "Introduction to Python programming for beginners",
    "slide_count": 6,
    "theme": "default"
})
print(response.json())

# List templates
templates = requests.get(f"{BASE_URL}/templates").json()
print(templates)

# Get a presentation by ID
presentation_id = response.json()["id"]
detail = requests.get(f"{BASE_URL}/presentation/{presentation_id}").json()
print(detail)
```

---

## Environment Variables

| Variable             | Default                                     | Description                         |
|----------------------|---------------------------------------------|-------------------------------------|
| `ANTHROPIC_API_KEY`  | *(required)*                                | Your Claude / Anthropic API key     |
| `APP_ENV`            | `development`                               | Application environment             |
| `APP_HOST`           | `0.0.0.0`                                   | Host address to bind to             |
| `APP_PORT`           | `8000`                                      | Port to listen on                   |
| `DEBUG`              | `true`                                      | Enable debug mode                   |
| `DATABASE_URL`       | `sqlite+aiosqlite:///./ppt_generator.db`    | SQLAlchemy database URL             |
| `UPLOAD_DIR`         | `uploads`                                   | Directory for temporary file uploads|
| `TEMPLATES_DIR`      | `app/templates`                             | Directory for template files        |
| `MAX_UPLOAD_SIZE_MB` | `50`                                        | Maximum upload file size in MB      |
| `ALLOWED_ORIGINS`    | `http://localhost:3000,http://localhost:8080`| Comma-separated CORS origins        |
