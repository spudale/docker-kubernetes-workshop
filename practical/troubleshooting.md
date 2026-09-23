# Troubleshooting Guide

## Docker Desktop is not running

Symptom:

```text
error during connect
```

Start Docker Desktop and wait for the engine to report that it is running.

## Port 8000 is already in use

Find the existing container:

```powershell
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

Use a different host port:

```powershell
docker run -p 8080:8000 docker-ml-api:v1
```

Then open <http://localhost:8080/docs>.

## Container exits immediately

```powershell
docker ps -a
docker logs CONTAINER_NAME
```

Common causes:

- missing `model.pkl`;
- dependency installation failure;
- incorrect `CMD`;
- invalid application import path.

## Kubernetes Pod shows ImagePullBackOff

```powershell
kubectl describe pod POD_NAME
```

Check:

- Docker Hub username;
- repository and tag;
- image visibility;
- internet access;
- `imagePullPolicy`.

## Pod shows CrashLoopBackOff

```powershell
kubectl logs POD_NAME
kubectl logs POD_NAME --previous
kubectl describe pod POD_NAME
```

## Service is unreachable

```powershell
kubectl get pods -l app=ml-api
kubectl get service ml-api
kubectl get endpoints ml-api
```

The Service selector and Pod labels must both be `app: ml-api`.

## Rollout does not complete

```powershell
kubectl rollout status deployment/ml-api
kubectl describe deployment ml-api
kubectl get pods
```

If the new image is broken:

```powershell
kubectl rollout undo deployment/ml-api
```

## Docker build cannot download Python packages

If the normal build fails with a TLS, proxy, or PyPI connectivity error, use
the included Linux wheel cache:

```powershell
docker build -f .\sample-app\Dockerfile.offline `
  -t docker-ml-api:v1 .\sample-app
```

The fallback is intended for x86-64 Docker Desktop workshop machines. Prefer
the standard `Dockerfile` whenever internet access works.
