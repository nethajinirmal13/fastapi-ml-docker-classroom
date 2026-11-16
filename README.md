# FastAPI + Machine Learning + Docker — Beginner Classroom Lab

A hands-on guided lab for **GitHub Codespaces**. Build a real FastAPI application that serves a small **scikit-learn LinearRegression** model inside a Docker container.

> **Teaching only:** All delivery records are synthetic. The predictions are not real-world delivery estimates. No API keys or paid services required.

## Learning outcomes

By the end of this lab, you can:
- Explain the difference between a **Dockerfile**, **image**, and **running container**.
- List app dependencies in `requirements.txt`.
- Train and package a model using `train_model.py` and `model.joblib`.
- Understand `EXPOSE 8000` versus `docker run -p 8000:8000`.
- Run GET and POST endpoints from Swagger UI, a browser, or `curl`.
- Observe FastAPI's validation errors (422) and business errors (400).
- Change code, rebuild the image, and compare image versions.

## Project files

| File | Purpose |
| --- | --- |
| `main.py` | FastAPI endpoints that load a trained model |
| `train_model.py` | Generates synthetic data and trains the regression model |
| `requirements.txt` | Pinned Python dependencies |
| `Dockerfile` | Installs dependencies, trains the model and starts the API |
| `.dockerignore` / `.gitignore` | Exclude unwanted files and secrets |
| `test_api.py` | Seven automated API tests |
| `.github/workflows/ci.yml` | Tests and Docker build on GitHub Actions |
| [Student worksheet](docs/STUDENT_WORKSHEET.md) | Copy-paste practice and checkpoints |
| [Instructor guide](docs/INSTRUCTOR_GUIDE.md) | 60–75 minute teaching sequence and troubleshooting |

## Quick start: GitHub Codespaces

1. Click **Code → Codespaces → Create codespace on main** on this repository.
2. Open the Codespaces terminal. The terminal should start in the repository root.
3. Check Docker:

   ```bash
   docker --version
   docker info
   docker run --rm hello-world
   ```

4. Build your ML Docker image:

   ```bash
   docker build -t delivery-ml:v1 .
   docker images
   ```

   During the build, the Dockerfile installs requirements and trains the synthetic delivery model. `RUN` steps happen at **build time**.

5. Start FastAPI in a container:

   ```bash
   docker run -d --name delivery-api -p 8000:8000 delivery-ml:v1
   docker ps
   docker logs delivery-api
   ```

6. Test from the same Codespace:

   ```bash
   curl http://127.0.0.1:8000/
   curl http://127.0.0.1:8000/model-info
   curl 'http://127.0.0.1:8000/predict-demo?distance_km=7&traffic=high&raining=true&orders_ahead=3'
   ```

7. Under **Ports**, open port **8000** in your signed-in browser and append `/docs` for Swagger UI. **Keep forwarded ports private.**

## Experiment 1 — Browser-friendly GET requests

Add these paths to your forwarded Codespaces URL:

```text
/predict-demo?distance_km=3&traffic=low&raining=false&orders_ahead=1
/predict-demo?distance_km=12&traffic=high&raining=true&orders_ahead=5
```

**Observe:** Which request takes longer according to the ML model?

## Experiment 2 — POST a JSON prediction

In `/docs`, select **POST /predict → Try it out** and execute:

```json
{
  "distance_km": 7,
  "traffic": "high",
  "raining": true,
  "orders_ahead": 3
}
```

Try the same API from the Codespaces terminal:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"distance_km":7,"traffic":"high","raining":true,"orders_ahead":3}'
```

**Observe:** Both clients receive JSON from the same API.

## Experiment 3 — Validation vs business errors

| Test URL path | Expected HTTP status | Reason |
| --- | --- | --- |
| `/predict-demo?distance_km=-5` | 422 | Pydantic validation rejects negative distance |
| `/predict-demo?distance_km=25` | 400 | FastAPI business rule restricts delivery to 20 km |
| `/predict-demo?distance_km=5&traffic=extreme` | 422 | Traffic must be low, medium or high |

## Experiment 4 — Port mapping

`EXPOSE 8000` documents the listening port **inside** the container. To reach the container from the Codespaces host, Docker needs `-p HOST_PORT:CONTAINER_PORT`.

```bash
docker stop delivery-api
docker rm delivery-api
docker run -d --name delivery-api -p 8080:8000 delivery-ml:v1
curl http://127.0.0.1:8080/
```

The app still runs on port **8000 inside** Docker, but the host now uses **8080**. Use port **8080** in the Codespaces Ports tab.

## Experiment 5 — Change code and rebuild

Edit the welcome message in `main.py`, then:

```bash
docker build -t delivery-ml:v2 .
docker stop delivery-api
docker rm delivery-api
docker run -d --name delivery-api -p 8080:8000 delivery-ml:v2
curl http://127.0.0.1:8080/
```

**Observe:** Changing source code does not modify an already built image. Rebuilding creates `v2`.

## Optional — Test without Docker

```bash
pip install -r requirements.txt pytest httpx
python train_model.py
python -m pytest -q
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The test suite checks the home endpoint, model metadata, GET and POST predictions, and three invalid requests.

## Cleanup

```bash
docker stop delivery-api
docker rm delivery-api
```

## Troubleshooting

| Problem | What to check |
| --- | --- |
| `docker: command not found` | Make sure Docker is available in your Codespace |
| Cannot connect to Docker daemon | Run `docker info` and inspect daemon availability |
| Port 8000 already allocated | Stop an older Uvicorn process or container, or use port 8080 |
| Container exits | Run `docker logs delivery-api` |
| Old response after editing code | Rebuild the image and restart a new container from the new tag |
| Missing `model.joblib` without Docker | Run `python train_model.py` before starting the API |
| Browser can't load API | Check `docker ps`, port forwarding, and that the correct port is open |

**Reminder:** Running a container inside Codespaces is a lab deployment, not permanent public hosting. Do not commit secrets or publish unnecessary ports.
