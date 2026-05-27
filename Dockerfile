FROM python:3.12.3-slim

WORKDIR /app

# install deps
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# create user
RUN useradd --system --no-create-home deploy_server

# switch user
USER deploy_server

EXPOSE 25381

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "25381"]