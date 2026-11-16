# Instructor guide — 60–75 minute live session

## Story

Yesterday students used FastAPI directly. Today they need to hand the same application to another developer without saying, "Install my exact Python setup manually." Docker provides an isolated, repeatable application environment.

**Analogy:** Dockerfile = recipe; image = packaged meal kit; container = kitchen running the recipe. `requirements.txt` is the ingredients list. `EXPOSE` documents the inside port; `-p` maps a host port so requests can reach it.

## Suggested delivery

| Time | Demo | Key question |
| --- | --- | --- |
| 0–10 min | `docker --version`, `hello-world` | Image vs container? |
| 10–20 min | `requirements.txt` + Dockerfile | Who installs libraries inside container? |
| 20–35 min | Build `delivery-ml:v1` | Why does model train during build? |
| 35–45 min | Run container, `docker ps`, logs | What starts on `docker run`? |
| 45–55 min | `/docs`, GET, POST, 400/422 | How does browser reach Python in Docker? |
| 55–65 min | 8080:8000 port switch | Which port changed? |
| 65–75 min | Change message, rebuild as v2 | Why rebuild instead of refresh? |

## Teacher's talk tracks

1. **Build vs run** — `RUN` lines in Dockerfile happen when building; `CMD` happens when the container starts.
2. **Container != VM** — containers share the host kernel, but isolate the application user space and processes.
3. **No production ML claims** — model uses synthetic data to demonstrate integration and reproducibility.
4. **Separate ML training & serving** — Docker build runs `train_model.py` and saves `model.joblib`. FastAPI loads it once during import; prediction requests do not retrain.
5. **422 vs 400** — 422 is input-format/constraint validation; 400 is an explicit out-of-service-area business rule.
6. **`EXPOSE` vs `-p`** — `EXPOSE 8000` documents the application port; `-p 8080:8000` publishes container port 8000 at host port 8080.
7. **Forwarded URL** — Codespaces port forwarding adds one more layer on top of the host port; use the Ports tab to open the browser link.

## Common mistakes and fixes

| Symptom | Check |
| --- | --- |
| `docker: command not found` | Docker unavailable in Codespace; choose a Docker-capable Codespace |
| `Cannot connect to Docker daemon` | Check `docker info` and availability of Docker service |
| `port is already allocated` | Stop yesterday's Uvicorn/container, or map to 8080 |
| `/docs` returns older routes | Check which application is running at forwarded port 8000 |
| `ModuleNotFoundError` during build | Confirm `requirements.txt` contains required package |
| `model.joblib not found` | Build from repository root; Dockerfile must run `python train_model.py` |
| Browser refuses connection | Check `docker ps`, `docker logs`, Codespaces Ports tab |
| Change to main.py not reflected | Rebuild image and start a new container with new version tag |
| `container name already in use` | Run `docker stop delivery-api && docker rm delivery-api` |

## Instructor checklist

- Confirm Docker available and port 8000 is free.
- Pre-build image if classroom network is slow (students should still see what building does).
- Keep port private; students can access their own Codespaces ports through signed-in browsers.
- Do not promise students a production deployment: the lab demonstrates containerized local/Codespaces execution.
