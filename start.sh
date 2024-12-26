#!/bin/bash

alembic upgrade head
uvicorn --factory src.main:setup_app --host 0.0.0.0 --port 8000 --reload
