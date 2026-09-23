# Docker and Kubernetes Command Cheat Sheet

## Docker

```powershell
docker version
docker build -t docker-ml-api:v1 .
docker images
docker run --name ml-api -p 8000:8000 docker-ml-api:v1
docker ps
docker ps -a
docker logs ml-api
docker exec -it ml-api sh
docker stop ml-api
docker rm ml-api
docker tag docker-ml-api:v1 USERNAME/docker-ml-api:v1
docker login
docker push USERNAME/docker-ml-api:v1
docker pull USERNAME/docker-ml-api:v1
```

## Kubernetes

```powershell
kind create cluster --name workshop --config .\kind-workshop-config.yaml
kind get clusters
kind get nodes --name workshop
kubectl config use-context kind-workshop
kubectl cluster-info
kubectl get nodes
kubectl apply -f .\kubernetes\deployment.yaml
kubectl apply -f .\kubernetes\service.yaml
kubectl get deployments
kubectl get pods -o wide
kubectl get services
kubectl describe pod POD_NAME
kubectl logs POD_NAME
kubectl scale deployment ml-api --replicas=3
kubectl delete pod POD_NAME
kubectl set image deployment/ml-api ml-api=USERNAME/docker-ml-api:v2
kubectl rollout status deployment/ml-api
kubectl rollout history deployment/ml-api
kubectl rollout undo deployment/ml-api
kubectl delete -f .\kubernetes
kind load docker-image docker-ml-api:v1 --name workshop
kind export logs .\kind-logs --name workshop
kind delete cluster --name workshop
```

## API test

```powershell
$body = @{
  study_hours = 7
  attendance = 85
  assignments_completed = 8
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8000/predict `
  -ContentType application/json `
  -Body $body
```
