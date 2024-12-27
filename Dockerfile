FROM python:3.12.6-slim as python-base

WORKDIR /tron

COPY /pyproject.toml /pyproject.toml

RUN pip install --upgrade pip \
  && pip install poetry \
  && poetry config virtualenvs.create false \
  && poetry install --no-dev

COPY . .

CMD ["uvicorn", "--factory", "src.main:setup_app", "--host", "0.0.0.0", "--port", "5000"]
