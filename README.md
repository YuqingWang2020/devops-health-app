# DevOps Health API – End-to-End Kubernetes Demo

## 1. Project Overview

This project is an end-to-end DevOps demonstration that covers the full lifecycle of a containerized application:
**development → containerization → Kubernetes deployment → configuration management → CI/CD automation → observability**.

The goal is not feature richness, but **operability and reliability**.
The application is intentionally minimal, while the surrounding infrastructure reflects real-world DevOps practices.

**Key objectives:**

* Run a stateless microservice in Kubernetes
* Fail fast on misconfiguration
* Enable self-healing via health probes
* Automate build and deployment
* Provide application-level observability

---

## 2. Architecture Overview

**High-level architecture:**

```
Developer
   │
   │ git push
   ▼
GitHub Repository
   │
   │ GitHub Actions (CI)
   ▼
Container Registry
   │
   │ Argo CD (GitOps)
   ▼
k3s Kubernetes Cluster
   │
   ├── Deployment (FastAPI Pod)
   │     ├── /health
   │     ├── /crash
   │     └── /metrics
   │
   ├── ConfigMap / Secret
   │
   └── Prometheus ──► Grafana
```

**Technology stack:**

* OS: Ubuntu 22.04
* Application: Python, FastAPI
* Containerization: Docker
* Orchestration: Kubernetes (k3s)
* CI: GitHub Actions
* CD / GitOps: Argo CD
* Monitoring: Prometheus, Grafana
* Packaging & Ops: Helm, Bash, YAML

---

**File Structure:**
```
devops-health-app/
├── app.py
├── Dockerfile
├── env
├── README.md
├── k8s/
      ├── Deployment.yaml
      ├── service.yaml
      ├── servicemonitor.yaml
├── argocd/
      ├── argocd-app.yaml
└── .github/workflows
      ├── ci.yaml
```

---

## 3. Application Behavior

The application is intentionally minimal to clearly demonstrate operational behavior.

### Endpoints

| Endpoint   | Purpose                             |
| ---------- | ----------------------------------- |
| `/`        | Basic service info                  |
| `/health`  | Health check for Kubernetes probes  |
| `/crash`   | Simulates a fatal application crash |
| `/metrics` | Prometheus metrics endpoint         |

### Fail-Fast Configuration

The application requires the environment variable `API_TOKEN`.
If the variable is missing, the application **terminates immediately on startup**.

**Rationale:**
Fail-fast behavior prevents partially misconfigured services from running and ensures Kubernetes can detect and handle failures deterministically.

---

## 4. Containerization (Docker)

The application is packaged as a Docker image to ensure consistency across environments.

**Key design choices:**

* Slim Python base image
* Single process per container
* Configuration via environment variables
* No embedded secrets

Example build and run:

```bash
docker build -t health-api .
docker run -e API_TOKEN=demo -p 8080:8080 health-api
```

---

## 5. Kubernetes Deployment

The service is deployed to a local **k3s Kubernetes cluster** using a `Deployment`.

### Core Kubernetes Concepts Used

* Deployment and ReplicaSet
* Pod lifecycle management
* Container ports and environment variables
* Health probes
* Rolling updates

### Health Probes

The Deployment defines both **liveness** and **readiness** probes:

* **Liveness probe:** ensures crashed containers are restarted
* **Readiness probe:** ensures traffic is only routed to healthy pods

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

---

## 6. Configuration Management (ConfigMap & Secret)

Configuration is externalized following Kubernetes best practices.

### ConfigMap

Used for non-sensitive configuration:

* `APP_ENV`
* `LOG_LEVEL`

### Secret

Used for sensitive configuration:

* `API_TOKEN`

All values are injected into the container via environment variables.

**Benefits:**

* No hardcoded configuration
* Clear separation of code and environment
* Secure handling of secrets

---

## 7. Failure Scenarios & Self-Healing

This project intentionally demonstrates failure handling.

### Simulated Crash

Calling the `/crash` endpoint immediately terminates the main process using `os._exit(1)`.

**Observed Kubernetes behavior:**

1. Container exits
2. Liveness probe fails
3. Kubernetes restarts the Pod
4. New Pod becomes Ready

This verifies Kubernetes’ **self-healing capability**.

---

## 8. CI/CD Pipeline

### Continuous Integration (CI)

Implemented using **GitHub Actions**.

On every push to `main`:

1. Source code is checked out
2. Docker image is built
3. Image is pushed to a container registry

This ensures:

* Reproducible builds
* Versioned artifacts
* No manual Docker builds

---

## 9. GitOps Deployment with Argo CD

Deployment is fully GitOps-driven.

* Kubernetes manifests are stored in Git
* Argo CD continuously monitors the repository
* Any change in manifests triggers automatic synchronization

**Advantages:**

* Declarative infrastructure
* Auditability via Git history
* No imperative `kubectl apply` from CI

---

## 10. Observability (Prometheus & Grafana)

### Metrics Exposure

The application exposes metrics at `/metrics` using `prometheus-client`.

Collected metrics include:

* HTTP request count
* Request latency histogram
* Metrics labeled by endpoint and method

### Prometheus Integration

* `ServiceMonitor` is used for automatic discovery
* Metrics are scraped every 15 seconds

### Grafana Dashboards

Custom dashboards visualize:

* Request rate (QPS)
* P95 request latency
* CPU usage per pod
* Pod restart count

This enables **end-to-end observability** from request behavior to infrastructure stability.

---

## 11. Operational Verification

Typical operational checks:

```bash
kubectl get pods
kubectl describe pod <pod>
kubectl logs <pod>
kubectl get events
kubectl exec -it <pod> -- sh
```

These commands cover the majority of real-world Kubernetes troubleshooting scenarios.

---

## 12. Key DevOps Concepts Demonstrated

* Stateless application design
* Fail-fast configuration
* Container lifecycle management
* Kubernetes self-healing
* Configuration and secret management
* CI/CD automation
* GitOps deployment model
* Application-level observability

---

## 13. Summary

This project demonstrates how a minimal application can be operated in a **production-oriented DevOps setup**.

The focus is not on application features, but on:

* Reliability
* Automation
* Observability
* Operational correctness

It reflects how I approach DevOps engineering in real-world environments.
