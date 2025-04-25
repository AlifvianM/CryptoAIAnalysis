FROM python:3.9

WORKDIR /app

# Install dependencies first (better layer caching)
COPY ./api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest
COPY ./api .

EXPOSE 8000 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]