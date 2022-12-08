FROM python:3.10-alpine

LABEL maintener="Ancelin Serre <dev_ancelin@outlook.com>"

WORKDIR /app/src

RUN python3 -m pip install -U pip

COPY src/database/ database/
COPY src/routers/ routers/
COPY src/app.py .
COPY src/crud.py .
COPY src/models.py . 
COPY src/schemas.py . 
COPY src/utils.py .

COPY requirements.txt /
RUN python -m pip install -r /requirements.txt


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]