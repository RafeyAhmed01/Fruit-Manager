# Fruit & Category Manager

A sleek minimal SaaS-style FastAPI + SQLAlchemy backend with a dynamic light/dark frontend.

## Features
- Dynamic web page with dropdown selectors (GET / POST / PUT / DELETE) and entity picker (Categories / Fruits)
- Night / day mode switcher (saved to localStorage)
- Clean glassmorphic card layout with gradient background
- Responsive navbar + footer (Rafey — GitHub link + copyright 2026)
- Real-time table rendering with conditional columns (Price / Quantity for fruits only)
- Validation (no pure-number names) with friendly error messages
- CORS-enabled for localhost development
- Pretty indented JSON for GET by ID (`Response` with `json.dumps`)
- Eager-loaded relationships (`joinedload`) to prevent `DetachedInstanceError`

## Routes (FastAPI — `back-end/src/app.py`)

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/categories` | List all categories |
| GET | `/categories/{id}` | Get category by ID |
| POST | `/categories` | Create category (`name`) |
| PUT | `/categories/{id}` | Update category (`name`; ID from URL/search bar) |
| DELETE | `/categories/{id}` | Delete category (blocked if linked fruits exist — 409 error) |
| GET | `/fruits` | List all fruits (with joined category) |
| GET | `/fruits/{id}` | Get fruit by ID (pretty indented JSON) |
| POST | `/fruits` | Create fruit (`name`, `category_id`, `price`, `quantity`) |
| PUT | `/fruits/{id}` | Update fruit (`name`, `category_id`, `price`, `quantity`) |
| DELETE | `/fruits/{id}` | Delete fruit |

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy ORM, SQLite (`sqlite:///fruit.db`), Pydantic v2 (`from_attributes = True`), pretty JSON via `starlette.Response`
- **Frontend:** Vanilla HTML/CSS/JS, gradient/glass theme, light/dark toggle, sticky navbar
- **DB:** `Category` (id, name) and `Fruit` (id, name, category_id, price, quantity) with relationships (`fruits` / `category`)

## How to Use
1. Start backend: `cd back-end && uvicorn src.app:app --reload`
2. Open `front-end/index.html` in browser (or serve via live server at `localhost:5500` etc)
3. Pick method + entity from dropdowns, enter params, click action button
4. Switch theme with the ☀ / 🌙 button (persists in `localStorage`)
5. For PUT / DELETE by ID, use the search input (Record ID in URL); for POST, use the param fields

## Install / Setup
```bash
# Backend
cd back-end
pip install -r requirements.txt
# Ensure SQLite DB exists: python -c "from src.db import create_tables; create_tables()"

# Frontend
# Just open front-end/index.html (fetches to http://localhost:8000)
```

## Project Structure
```
back-end/src/app.py   # FastAPI routes + CORS
back-end/src/db.py    # SQLAlchemy models + session
back-end/src/schemas.py  # Pydantic v2 schemas (from_attributes = True)
front-end/index.html  # Dynamic UI (dropdowns, table, theme button)
front-end/app.js     # Build payload, fetch, render table
front-end/style.css  # Minimal SaaS theme with light/dark variables
```

## Credits
- Created by Rafey — [GitHub](https://github.com/RafeyAhmed01)
- Copyright 2026 — Fruit & Category Manager
