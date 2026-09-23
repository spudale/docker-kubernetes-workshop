# Docker and Kubernetes Concepts Reference

## Containerization vocabulary

| Term | Meaning |
| --- | --- |
| Container | Isolated application process created from an image |
| Image | Immutable, versioned application package |
| Layer | Reusable filesystem change in an image |
| Registry | Service that stores and distributes images |
| Repository | Collection of image versions under one registry name |
| Tag | Human-readable image version such as `v1` |
| Volume | Persistent or shared container data |
| Network | Communication boundary for containers |

## Kubernetes vocabulary

| Term | Meaning |
| --- | --- |
| Cluster | Control plane and worker nodes |
| Node | Machine that runs Pods |
| Pod | Smallest deployable unit |
| ReplicaSet | Maintains a number of equivalent Pods |
| Deployment | Manages ReplicaSets and rolling updates |
| Service | Stable endpoint for a changing set of Pods |
| Namespace | Logical object grouping |
| Label | Key/value metadata used for selection |
| Probe | Health check used by Kubernetes |

## Desired state

Kubernetes is declarative. The manifest states what should exist:

```yaml
spec:
  replicas: 3
```

Controllers compare that desired state with reality. If only two Pods exist,
Kubernetes creates another. This repeated comparison is called reconciliation.

## Readiness versus liveness

- **Readiness probe:** Can this Pod receive traffic now?
- **Liveness probe:** Is this container stuck and in need of restart?

A failing readiness probe removes a Pod from Service endpoints. A failing
liveness probe restarts the container.

## Scaling

Horizontal scaling changes the number of application replicas:

```powershell
kubectl scale deployment ml-api --replicas=3
```

This improves capacity and availability only when the application can safely
run as multiple instances.

## Self-healing

Deleting a Pod does not change the Deployment's desired replica count. The
Deployment controller creates a replacement Pod.

## Rolling update

When a Deployment image changes, Kubernetes gradually creates new Pods and
removes old Pods. Readiness checks prevent traffic from reaching a new Pod
before it is ready.

```powershell
kubectl set image deployment/ml-api `
  ml-api=USERNAME/docker-ml-api:v2
kubectl rollout status deployment/ml-api
kubectl rollout undo deployment/ml-api
```

## Production topics intentionally out of scope

Mention these briefly, but do not teach them in depth during this workshop:

- Helm and operators;
- ingress controllers;
- persistent storage;
- autoscaling internals;
- service meshes;
- network policies;
- production secret-management systems;
- multi-cluster deployment.

