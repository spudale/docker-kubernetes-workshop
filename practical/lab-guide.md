# Hands-on Lab: ML API from Laptop to Kubernetes

**Duration:** 1:00 PM-3:00 PM  
**Working directory:** `docker-kubernetes-workshop`

## Lab 1 — Run the ML API locally

Generate the pre-trained model:

```powershell
python .\sample-app\train_model.py
```

Create an environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r .\sample-app\requirements.txt
```

Start the API:

```powershell
python -m uvicorn app.main:app `
  --app-dir .\sample-app `
  --host 127.0.0.1 `
  --port 8000
```

Open <http://localhost:8000/docs> and execute `POST /predict`.

Checkpoint:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

Stop the API with `Ctrl+C`.

## Lab 2 — Understand the Dockerfile

Open `sample-app/Dockerfile`.

Identify:

1. base image;
2. working directory;
3. dependency installation;
4. source-code copy;
5. application port;
6. startup command.

Build the image:

```powershell
docker build -t docker-ml-api:v1 .\sample-app
docker images docker-ml-api
```

For an offline build, use the offline Dockerfile:

```powershell
docker build -f .\sample-app\Dockerfile.offline -t docker-ml-api:v1 .\sample-app
```

## Lab 3 — Run and inspect the container

First run the intentionally incomplete command:

```powershell
docker run --name ml-api-broken docker-ml-api:v1
```

In another terminal, try <http://localhost:8000/health>. It is unreachable
because no host port was published.

Stop and remove it:

```powershell
docker stop ml-api-broken
docker rm ml-api-broken
```

Run it correctly:

```powershell
docker run --name ml-api -d -p 8000:8000 docker-ml-api:v1
docker ps
docker logs ml-api
docker port ml-api
```

Test it:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

Submit a prediction using the command in the cheat sheet.

Cleanup:

```powershell
docker stop ml-api
docker rm ml-api
```

## Lab 4 — Push to Docker Hub

Replace `USERNAME`:

```powershell
docker login
docker tag docker-ml-api:v1 USERNAME/docker-ml-api:v1
docker push USERNAME/docker-ml-api:v1
```

Open Docker Hub and confirm the `v1` tag exists.

Optional proof:

```powershell
docker rmi USERNAME/docker-ml-api:v1
docker pull USERNAME/docker-ml-api:v1
```

## Lab 5 — Deploy to Kubernetes

Edit `kubernetes/deployment.yaml` and replace
`YOUR_DOCKERHUB_USERNAME`.

Apply the Deployment:

```powershell
kubectl apply -f .\kubernetes\deployment.yaml
kubectl get deployments
kubectl get pods -l app=ml-api -w
```

Wait until the Pod is `Running` and Ready (`1/1`). Press `Ctrl+C` to stop
watching.

Inspect:

```powershell
kubectl describe deployment ml-api
kubectl logs deployment/ml-api
```

## Lab 6 — Expose the API

```powershell
kubectl apply -f .\kubernetes\service.yaml
kubectl get service ml-api
```

Alternatively, start a temporary port forward:

```powershell
kubectl port-forward service/ml-api 8080:8000
```

The workshop kind cluster maps NodePort `30080` to host port `8080`. Test:

```powershell
Invoke-RestMethod http://localhost:8080/health
```

Use `http://localhost:8080` for `/health`, `/docs`, and `/predict`.

## Lab 7 — Scale

```powershell
kubectl scale deployment ml-api --replicas=3
kubectl get pods -l app=ml-api -o wide
```

Observe that all Pods use the same image but have different names and IPs.

## Lab 8 — Observe self-healing

List Pods:

```powershell
kubectl get pods -l app=ml-api
```

Delete one:

```powershell
kubectl delete pod POD_NAME
kubectl get pods -l app=ml-api -w
```

Kubernetes creates a replacement because the Deployment still requests three
replicas.

## Lab 9 — Perform a rolling update

Edit `sample-app/app/main.py` and change:

```python
MODEL_VERSION = "v1"
```

to:

```python
MODEL_VERSION = "v2"
```

Build and push:

```powershell
docker build -t USERNAME/docker-ml-api:v2 .\sample-app
docker push USERNAME/docker-ml-api:v2
```

Update Kubernetes:

```powershell
kubectl set image deployment/ml-api `
  ml-api=USERNAME/docker-ml-api:v2
kubectl rollout status deployment/ml-api
kubectl get pods -l app=ml-api
```

Call `/health` and confirm `model_version` is `v2`.

Rollback exercise:

```powershell
kubectl rollout undo deployment/ml-api
kubectl rollout status deployment/ml-api
```

## Lab 10 — Connect to the industry workflow

Explain each workshop artifact:

| Workshop artifact | Industry equivalent |
| --- | --- |
| Laptop source code | Git repository |
| `docker build` | CI pipeline |
| Docker Hub | Enterprise container registry |
| Local Kubernetes | Managed cloud/on-prem cluster |
| Manual image update | CD or GitOps deployment |
| `kubectl get/logs` | Operational troubleshooting |
| Scaling and probes | Reliability engineering |

## Cleanup

```powershell
kubectl delete -f .\kubernetes
docker image prune
```

Delete the local workshop cluster when it is no longer needed:

```powershell
kind delete cluster --name workshop
```

Do not run broad cleanup commands on a shared machine.
