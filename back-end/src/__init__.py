"""
Fruit Management API

A simple FastAPI API to manage fruits using PostgreSQL and SQLAlchemy.

This package contains:
- main.py: FastAPI application with CRUD endpoints
- db.py: SQLAlchemy database models and operations
- schemas.py: Pydantic models for API validation
"""

__version__ = "0.1.0"

__all__ = ["main", "db", "schemas"]