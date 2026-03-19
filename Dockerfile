FROM python:3.13-slim

WORKDIR /travel_planner

COPY requirements.txt .

RUN python -m pip install --upgrade pip &&\
    pip install --no-cache-dir -r requirements.txt

COPY ./app /travel_planner/app

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]