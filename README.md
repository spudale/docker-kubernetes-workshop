# Docker and Kubernetes Workshop

Build a Python ML API, package it with Docker, publish it to Docker Hub, and
deploy it to a local Kubernetes cluster created with
[kind](https://kind.sigs.k8s.io/).

## Workshop flow

```text
Python ML API -> Docker image -> Docker Hub -> kind Kubernetes cluster
              -> Deployment -> Service -> Scaling -> Rolling update
```

## Learning outcomes

By the end of the workshop, students will be able to:

- explain containers, images, registries, Pods, Deployments, and Services;
- build and run a Docker image;
- inspect container status and logs;
- tag and push an image to Docker Hub;
- create a local Kubernetes cluster with kind;
- deploy and expose an application on Kubernetes;
- scale replicas and observe self-healing;
- perform and roll back a rolling update.

## Repository structure

| Directory or file | Purpose |
| --- | --- |
| `student/` | Detailed prerequisites and command cheat sheet |
| `theory/` | Theory session guide and concept reference |
| `practical/` | Step-by-step lab and troubleshooting guide |
| `sample-app/` | FastAPI application, model, tests, and Dockerfiles |
| `kubernetes/` | Kubernetes Deployment and Service manifests |
| `scripts/` | Workshop preflight and API test scripts |
| `kind-workshop-config.yaml` | Reproducible local Kubernetes cluster configuration |

## Student preparation

Complete [student/prerequisites.md](student/prerequisites.md) before the
workshop. The essential tools are:

- Docker Desktop or Docker Engine;
- Python 3.10 or later;
- Git;
- Visual Studio Code;
- `kubectl`;
- kind;
- a verified Docker Hub account.

A GitHub account is only required when the workshop repository is private or
students need to fork and submit their work through GitHub.

## Get the workshop

Clone the repository:

```text
git clone <REPOSITORY_URL>
cd docker-kubernetes-workshop
```

Alternatively, download the repository ZIP from GitHub and extract it before
running any commands.

## Check your environment

On Windows, run:

```powershell
.\scripts\preflight.ps1
```

The script verifies Docker, Python, Git, `kubectl`, kind, and the active
Kubernetes cluster.

## Create the kind cluster

Ensure Docker is running, then execute:

```text
kind create cluster --name workshop --config kind-workshop-config.yaml
kubectl config use-context kind-workshop
kubectl wait --for=condition=Ready nodes --all --timeout=180s
kubectl get nodes
```

The cluster maps Kubernetes NodePort `30080` to
<http://localhost:8080> on the host.

## Run the application locally

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\sample-app\requirements.txt
python -m uvicorn app.main:app --app-dir .\sample-app --reload
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r ./sample-app/requirements.txt
python -m uvicorn app.main:app --app-dir ./sample-app --reload
```

Open:

- API documentation: <http://localhost:8000/docs>
- Health endpoint: <http://localhost:8000/health>

## Start the hands-on lab

Follow [practical/lab-guide.md](practical/lab-guide.md). Replace:

- `USERNAME` in command examples with your Docker Hub username;
- `YOUR_DOCKERHUB_USERNAME` in
  [`kubernetes/deployment.yaml`](kubernetes/deployment.yaml) with the same
  username.

For common errors, see
[practical/troubleshooting.md](practical/troubleshooting.md).

## Clean up

Remove workshop workloads:

```text
kubectl delete -f kubernetes
```

Delete the complete local cluster:

```text
kind delete cluster --name workshop
```

## Workshop schedule

| Session | Time | Purpose |
| --- | --- | --- |
| Theory | 10:00 AM-12:00 PM | Docker and Kubernetes concepts |
| Hands-on | 1:00 PM-3:00 PM | Containerize and deploy the ML API |

Prepared for PCET's Nutan Maharashtra Institute of Engineering and Technology,
28 September 2026.
