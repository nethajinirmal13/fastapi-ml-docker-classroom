# 1. Start with Python (the container's own Python runtime)
FROM python:3.11-slim

# 2. Create a working folder INSIDE the image
WORKDIR /app

# 3. Install dependencies listed by the project
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Train a small synthetic ML model DURING image build
COPY train_model.py .
RUN python train_model.py

# 5. Copy the FastAPI application into the image
COPY main.py .

# 6. Use an unprivileged user to run the server
RUN useradd --uid 10001 --create-home appuser
USER appuser

# 7. Document the listening port (actual publication uses docker -p)
EXPOSE 8000

# 8. Start API when the container starts; NOT --reload in a container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
