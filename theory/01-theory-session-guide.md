# Theory Session Guide

**Duration:** 10:00 AM-12:00 PM  
**Rule:** Explain only concepts used in the afternoon lab.

## 10:00-10:10 — Opening and workshop story

### Learning objective

Students understand the problem the workshop solves and the final deployment
workflow.

### Opening question

> "If an application works on a developer's laptop, why might it fail on
> another laptop or in production?"

Expected answers include different Python versions, missing libraries,
operating-system differences, configuration, and networking.

### Core message

Docker packages an application with its runtime and dependencies. Kubernetes
keeps multiple containers running reliably across machines.

```text
Source code
    ↓
Dockerfile
    ↓
Docker image
    ↓
Container registry
    ↓
Kubernetes Deployment
    ↓
Pods + Service
```

## 10:10-10:30 — Containers and virtual machines

### What is a container?

A container is an isolated process with its application files, dependencies,
configuration, and a restricted view of operating-system resources.

Containers share the host operating-system kernel. They do not package a full
guest operating system.

### Container benefits

- consistent runtime from development to production;
- fast startup and lower overhead than most virtual machines;
- immutable, versioned application packaging;
- process and dependency isolation;
- convenient scaling and replacement;
- portability across compatible container platforms.

### Containers versus virtual machines

| Virtual machine | Container |
| --- | --- |
| Includes a guest operating system | Shares the host kernel |
| Usually larger and slower to start | Usually smaller and faster |
| Strong machine-level isolation | Process-level isolation |
| Good for different operating systems | Good for packaging applications |
| Managed as long-lived machines | Commonly treated as replaceable instances |

Avoid saying that containers are "lightweight virtual machines." Their
isolation and operating model are different.

### Industry examples

- microservice APIs;
- CI/CD build agents;
- scheduled data-processing jobs;
- web frontends;
- model-inference APIs;
- developer environments.

## 10:30-10:50 — Docker architecture

### Components

**Docker Client**  
The `docker` command sends requests to the Docker Engine.

**Docker Engine / daemon**  
Builds images, creates networks and volumes, and manages containers.

**Image**  
A read-only, versioned template composed of filesystem layers.

**Container**  
A running or stopped instance of an image with a writable layer.

**Registry**  
A remote service that stores and distributes images. Docker Hub is a public
registry.

### Request flow

```text
docker run my-api:v1
       │
       ▼
Docker Client -> Docker Engine -> local image?
                                    │ no
                                    ▼
                                Docker Hub
```

### Important distinction

An image is a packaged artifact. A container is a process created from that
artifact. One image can create many containers.

## 10:50-11:15 — Images, containers, and Dockerfiles

### Container lifecycle

```text
created -> running -> stopped -> removed
                └── restart ──┘
```

### Commands used in the practical

```powershell
docker build -t docker-ml-api:v1 .
docker images
docker run --name ml-api -p 8000:8000 docker-ml-api:v1
docker ps
docker logs ml-api
docker stop ml-api
docker rm ml-api
```

### Dockerfile instructions

| Instruction | Purpose |
| --- | --- |
| `FROM` | Select the base image |
| `WORKDIR` | Set the working directory |
| `COPY` | Copy application files into the image |
| `RUN` | Execute a build-time command |
| `EXPOSE` | Document the application port |
| `ENV` | Define an environment variable |
| `CMD` | Define the default container process |

### Layer and cache explanation

Each relevant Dockerfile instruction creates a layer. Put stable dependency
files before frequently changing source files so Docker can reuse cached
layers.

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app ./app
```

### Image design guidance

- use a small, trusted base image;
- pin important dependency versions;
- do not place secrets in the image;
- use `.dockerignore`;
- run one main application process per container;
- use explicit image tags.

## 11:15-11:30 — Networking, ports, logs, and registries

### Port mapping

The API listens on port `8000` inside the container. The mapping below exposes
it as port `8000` on the student's computer:

```powershell
docker run -p 8000:8000 docker-ml-api:v1
```

The first port is the host port; the second is the container port.

### Troubleshooting flow

1. Is the container running? `docker ps -a`
2. What did the application print? `docker logs <name>`
3. Is the correct port mapped? `docker port <name>`
4. Is the application listening on `0.0.0.0`, not only `127.0.0.1`?
5. Is the request path correct?

### Registry workflow

```powershell
docker login
docker tag docker-ml-api:v1 USERNAME/docker-ml-api:v1
docker push USERNAME/docker-ml-api:v1
docker pull USERNAME/docker-ml-api:v1
```

Never use `latest` as the only production version identifier.

## 11:30-11:48 — Why Kubernetes?

Docker runs containers. Kubernetes coordinates containers across a cluster.

Kubernetes helps with:

- desired-state deployment;
- replica management;
- service discovery and stable networking;
- self-healing;
- rolling updates and rollback;
- configuration and secret integration;
- scheduling based on available resources.

### Kubernetes architecture

**Cluster**  
The complete Kubernetes environment.

**Control plane**  
Stores desired state and makes cluster-wide decisions.

**API server**  
The entry point for `kubectl` and other clients.

**Scheduler**  
Selects a suitable node for each new Pod.

**Controller manager**  
Continuously reconciles actual state with desired state.

**etcd**  
Stores cluster configuration and state.

**Worker node**  
Runs application Pods.

**kubelet**  
Ensures assigned Pods are running on its node.

## 11:48-12:00 — Core objects and complete workflow

### Pod

The smallest deployable Kubernetes unit. A Pod usually contains one main
application container. Pods are replaceable and receive temporary IP
addresses.

### Deployment

Declares the desired image and replica count. It creates ReplicaSets, replaces
failed Pods, and performs rolling updates.

### Service

Provides a stable network endpoint and distributes traffic across matching
Pods.

### Labels and selectors

Labels identify objects. Selectors connect Services and Deployments to the
correct Pods.

```text
Service selector: app=ml-api
             │
             ├── Pod label: app=ml-api
             ├── Pod label: app=ml-api
             └── Pod label: app=ml-api
```

### Docker and Kubernetes together

| Docker responsibility | Kubernetes responsibility |
| --- | --- |
| Build the image | Schedule Pods |
| Run a local container | Maintain replica count |
| Push/pull from registry | Pull images onto nodes |
| Local port mapping | Stable Service networking |
| Inspect one container | Coordinate an application deployment |

### End with the afternoon challenge

> "We will take one FastAPI machine-learning service from local Python to
> Docker, Docker Hub, Kubernetes, three replicas, self-healing, and a rolling
> update."

