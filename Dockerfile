FROM python:3.10-slim

WORKDIR /app/

COPY requirements/requirements.txt requirements/requirements-prod.txt /app/requirements/
RUN pip install -r /app/requirements/requirements.txt && pip install -r /app/requirements/requirements-prod.txt

# copy code and models
#ADD models /app/models
ADD src /app/src
WORKDIR /app

COPY .env /app/.env

ENV PYTHONPATH="${PYTHONPATH}:/app/src/hackacity2022"

# The code to run when container is started
CMD python src/hackacity2022/api.py
