# Student worksheet — Docker + FastAPI ML hands-on

**Goal:** In your own GitHub Codespace, run an ML prediction API inside Docker and explain each step in simple terms.

## Lab 0: Check your environment

```bash
docker --version
docker info
docker run --rm hello-world
```

Checkpoint: A `hello-world` container runs successfully.

## Lab 1: Identify the packaging files

Open `requirements.txt`, `Dockerfile`, `train_model.py`, `main.py`.

Fill in:
- Where does Python get installed? ________
- Where are the Python packages listed? ________
- When is the ML model trained? ________
- Which file defines the API endpoints? ________
- Which instruction tells the container which command starts FastAPI? ________

## Lab 2: Build the Docker image

```bash
docker build -t delivery-ml:v1 .
docker images
```

Checkpoint: Find the `delivery-ml` image.

Predict: Did this command start a web server yet? ________

## Lab 3: Run the container and test the API

```bash
docker run -d --name delivery-api -p 8000:8000 delivery-ml:v1
docker ps
docker logs delivery-api
curl http://127.0.0.1:8000/
```

In Ports, open port 8000 in the browser and add `/docs`. Test `POST /predict` with:

```json
{"distance_km": 7, "traffic": "high", "raining": true, "orders_ahead": 3}
```

Checkpoint: Write down your estimated minutes: ________

## Lab 4: Make the API respond to different situations

Test these GET paths in your forwarded URL:

```
/predict-demo?distance_km=3&traffic=low&raining=false&orders_ahead=1
/predict-demo?distance_km=12&traffic=high&raining=true&orders_ahead=5
/predict-demo?distance_km=-1
/predict-demo?distance_km=25
/predict-demo?distance_km=5&traffic=extreme
```

Explain: Why are the last three requests rejected? ________

## Lab 5: Experiment with port mapping

```bash
docker stop delivery-api
docker rm delivery-api
docker run -d --name delivery-api -p 8080:8000 delivery-ml:v1
curl http://127.0.0.1:8080/
```

What changed: the host port or the container port? ________

## Lab 6: Change source code and rebuild

Change the message in the `home()` function in `main.py`. Then:

```bash
docker build -t delivery-ml:v2 .
docker stop delivery-api
docker rm delivery-api
docker run -d --name delivery-api -p 8080:8000 delivery-ml:v2
curl http://127.0.0.1:8080/
```

Checkpoint: The updated message appears.

## Extra: Test without Docker

```bash
pip install -r requirements.txt pytest httpx
python train_model.py
python -m pytest -q
```

Checkpoint: All seven tests pass.

## Cleanup

```bash
docker stop delivery-api
docker rm delivery-api
```

**In one sentence:** A Docker image is ________, while a Docker container is ________.
