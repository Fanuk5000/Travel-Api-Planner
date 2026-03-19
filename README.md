# Travel Planner API

A backend RESTful API built with **FastAPI** and **SQLite**, designed to help travellers plan projects and curate lists of places to visit. This project fulfills the Travel Company engineering assessment, including third-party integration with the Art Institute of Chicago API.

## 🚀 Features & Business Logic Implemented

- **CRUD Operations:** Full lifecycle management for Travel Projects and Places.
- **External API Validation:** Asynchronously validates artworks against the Art Institute of Chicago API before adding them to a project.
- **Constraints Enforced:**
  - Maximum of 10 places per project.
  - Projects cannot be deleted if any of their places are marked as `visited`.
  - Prevents adding duplicate places (same `external_id`) to the same project.
  - Dynamically computes `is_completed` to `true` when all places in a project are visited.
- **Bonus Features Included:**
  - Clean, modular project structure (separated routers/endpoints).
  - Dockerized for easy local development and production simulation.
  - Pagination on the `GET /projects/` list endpoint.

## 📂 Project Structure

```text
travel_planner/
├── app/
│   ├── routers/
│   │   ├── projects.py    # Project endpoints
│   │   └── places.py      # Places endpoints
│   ├── database.py        # SQLite setup & session management
│   ├── main.py            # FastAPI application factory
│   ├── models.py          # SQLAlchemy ORM models
│   ├── schemas.py         # Pydantic validation models
│   └── utils.py           # Shared logic (External API validation)
├── .dockerignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```
