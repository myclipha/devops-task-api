# DevOps Task API

A containerized FastAPI task management API deployed to Kubernetes with MongoDB persistence, GitHub Actions CI, GitHub Container Registry, and Argo CD GitOps.

## Project Overview

This project demonstrates a complete containerized application delivery workflow:

* Develop and test a FastAPI application
* Containerize the application with Docker
* Run the application on Kubernetes
* Persist MongoDB data using a PersistentVolumeClaim
* Manage application configuration with ConfigMaps and Secrets
* Build and publish Docker images with GitHub Actions
* Store immutable container images in GitHub Container Registry (GHCR)
* Deploy and reconcile Kubernetes resources with Argo CD
* Apply Kubernetes RBAC and NetworkPolicy
* Harden the application container using Kubernetes security controls
* Troubleshoot Kubernetes deployment and container security issues

## Architecture

```text
                    GitHub Repository
                           |
                           v
                   GitHub Actions CI
                    /             \
                   v               v
              Run pytest        Build Docker
                                    |
                                    v
                                  GHCR
                                    |
                                    v
                              Argo CD GitOps
                                    |
                                    v
                            Kubernetes Cluster
                                    |
                 +------------------+------------------+
                 |                                     |
                 v                                     v
        FastAPI Deployment                    MongoDB Deployment
             2 replicas                              |
                 |                                    v
                 |                              MongoDB Service
                 v                                    |
        FastAPI Service                              v
                 |                              PersistentVolume
                 +-------------> MongoDB              |
                                      |               v
                                      +------------> PVC
```

## Application

The API is built with:

* Python
* FastAPI
* Uvicorn
* PyMongo
* Pytest

### API Endpoints

| Method | Endpoint           | Purpose                      |
| ------ | ------------------ | ---------------------------- |
| GET    | `/`                | Application status           |
| GET    | `/health`          | API and MongoDB health check |
| GET    | `/tasks`           | Retrieve tasks               |
| POST   | `/tasks`           | Create a task                |
| PUT    | `/tasks/{task_id}` | Update a task                |
| DELETE | `/tasks/{task_id}` | Delete a task                |

## Containerization

The application is packaged as a Docker image using `python:3.12-slim`.

The container is hardened to run as a non-root user:

```dockerfile
USER 1000:1000
```

The image is published to GitHub Container Registry using immutable Git commit SHA tags.

Example:

```text
ghcr.io/myclipha/devops-task-api:<commit-sha>
```

## Kubernetes

The application is deployed to a local Kubernetes cluster using Docker Desktop Kubernetes.

Kubernetes resources include:

* Deployment
* Service
* ConfigMap
* Secret
* PersistentVolumeClaim
* NetworkPolicy
* ServiceAccount
* Role
* RoleBinding

The FastAPI deployment runs two replicas.

MongoDB uses a PersistentVolumeClaim mounted at:

```text
/data/db
```

## Configuration and Secrets

Application configuration is managed using a Kubernetes ConfigMap.

Database credentials are provided through a Kubernetes Secret rather than being hard-coded into the application deployment.

The local secret manifest is excluded from Git using `.gitignore`.

## Kubernetes Security

The FastAPI deployment uses several container security controls:

```yaml
runAsNonRoot: true
seccompProfile:
  type: RuntimeDefault
```

The container also uses:

```yaml
allowPrivilegeEscalation: false
readOnlyRootFilesystem: true
capabilities:
  drop:
    - ALL
```

The running container was verified to execute as a non-root user with UID 1000.

## NetworkPolicy

A Kubernetes NetworkPolicy restricts MongoDB ingress traffic so that MongoDB accepts connections from the FastAPI application pods.

The API-to-MongoDB connection was tested after applying the policy.

## RBAC

A dedicated Kubernetes ServiceAccount, Role, and RoleBinding were created for a read-only workload identity.

The role permits:

```text
pods:
  get
  list
  watch
```

The ServiceAccount was verified to:

* Get pods
* List pods
* Watch pods

It cannot:

* Delete pods
* Create deployments

## CI/CD

GitHub Actions performs the following workflow:

```text
Git push
   |
   v
Checkout source
   |
   v
Install Python dependencies
   |
   v
Run pytest
   |
   v
Authenticate to GHCR
   |
   v
Build Docker image
   |
   v
Push image tagged with Git commit SHA
```

The workflow runs automatically for changes pushed to `main` and for pull requests targeting `main`.

## GitOps with Argo CD

Argo CD monitors the Kubernetes manifests stored in the Git repository.

The deployment flow is:

```text
Git commit
    |
    v
GitHub Actions
    |
    v
GHCR image
    |
    v
Kubernetes manifest updated
    |
    v
Argo CD detects Git change
    |
    v
Kubernetes Deployment updated
```

Argo CD is configured for automated synchronization, pruning, and self-healing.

The application's Argo CD status has been verified as:

```text
Synced | Healthy | Succeeded
```

Argo CD self-healing was also tested by manually changing the deployment replica count and observing Argo CD restore the desired state.

## Troubleshooting Example

During container security hardening, Kubernetes rejected an image because the configured non-root user could not be verified when the image specified a username directly.

The issue was investigated through:

```text
Pod status
    |
    v
ReplicaSet
    |
    v
Deployment image
    |
    v
Docker image user configuration
```

The container was changed to use an explicit numeric UID:

```dockerfile
USER 1000:1000
```

A new image was built and published through GitHub Actions, the immutable image reference was updated in Git, and Argo CD deployed the new version.

The running pod was then verified with:

```bash
kubectl exec deploy/devops-task-api -- id
```

and the application health endpoint confirmed that the API could still connect to MongoDB.

## Infrastructure as Code

Terraform configuration has been created for an Azure resource group.

Terraform was used to:

* Initialize the project
* Validate the configuration
* Generate an execution plan
* Investigate Azure authorization requirements

The Azure resource creation was not completed because the current Azure account does not have sufficient subscription-level permissions.

## Testing

Application tests are executed with:

```bash
python -m pytest
```

The API was also tested inside Kubernetes through its health endpoint:

```text
/health
```

The health check verifies both application availability and MongoDB connectivity.

## Technologies

* Python
* FastAPI
* MongoDB
* Docker
* Kubernetes
* Git
* GitHub
* GitHub Actions
* GitHub Container Registry
* Argo CD
* Terraform
* Azure CLI

## Project Goals

This project is intended as a hands-on DevOps learning and portfolio project focused on:

* Containerization
* Kubernetes operations
* CI/CD
* GitOps
* Infrastructure as Code
* Container security
* Kubernetes RBAC
* Network security
* Persistent storage
* Troubleshooting and operational validation

