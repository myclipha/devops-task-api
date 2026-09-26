# DevOps Task API

A containerized FastAPI task management API deployed to Kubernetes with MongoDB persistence.

## Architecture

```text
Client
  |
  v
Kubernetes Service
  |
  v
FastAPI Pods (2 replicas)
  |
  v
MongoDB Service
  |
  v
MongoDB Pod
  |
  v
PersistentVolumeClaim

