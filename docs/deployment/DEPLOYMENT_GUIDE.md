# Deployment Guide

## Infrastructure Setup

### Prerequisites
- Google Cloud Platform account
- `gcloud` CLI installed
- `kubectl` installed
- Docker installed
- Helm installed

### Initial Setup

1. Create GCP Project
```bash
gcloud projects create hexproperty-prod
gcloud config set project hexproperty-prod
```

2. Enable Required APIs
```bash
gcloud services enable container.googleapis.com
gcloud services enable sql.googleapis.com
gcloud services enable redis.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

3. Create GKE Cluster
```bash
gcloud container clusters create hexproperty-cluster \
    --region us-central1 \
    --num-nodes 3 \
    --machine-type e2-standard-4 \
    --enable-autoscaling \
    --min-nodes 3 \
    --max-nodes 10
```

## Database Setup

### PostgreSQL
1. Create Cloud SQL instance
```bash
gcloud sql instances create hexproperty-postgres \
    --database-version=POSTGRES_13 \
    --region=us-central1 \
    --tier=db-custom-4-16384 \
    --storage-type=SSD \
    --storage-size=100GB
```

2. Create databases
```bash
gcloud sql databases create property_db --instance=hexproperty-postgres
gcloud sql databases create tenant_db --instance=hexproperty-postgres
gcloud sql databases create lease_db --instance=hexproperty-postgres
```

### MongoDB
1. Set up MongoDB Atlas cluster
2. Configure network access
3. Create database users
4. Initialize collections

## Cache Layer

### Redis Setup
```bash
gcloud redis instances create hexproperty-redis \
    --size=5 \
    --region=us-central1 \
    --redis-version=redis_6_x
```

## Message Queue

### Kafka Setup
1. Create Kafka cluster using Confluent Cloud
2. Configure topics:
   - property-events
   - tenant-events
   - lease-events
   - billing-events

## Search Engine

### Elasticsearch Setup
1. Deploy Elasticsearch using Helm:
```bash
helm repo add elastic https://helm.elastic.co
helm install elasticsearch elastic/elasticsearch \
    --set replicas=3 \
    --set resources.requests.cpu=1000m \
    --set resources.limits.cpu=2000m \
    --set resources.requests.memory=2Gi \
    --set resources.limits.memory=4Gi
```

## Application Deployment

### 1. Frontend Deployment
```bash
kubectl apply -f k8s/frontend/deployment.yaml
kubectl apply -f k8s/frontend/service.yaml
kubectl apply -f k8s/frontend/ingress.yaml
```

### 2. Backend Services
```bash
kubectl apply -f k8s/backend/property-service/
kubectl apply -f k8s/backend/tenant-service/
kubectl apply -f k8s/backend/lease-service/
kubectl apply -f k8s/backend/billing-service/
```

### 3. Support Services
```bash
kubectl apply -f k8s/support/monitoring/
kubectl apply -f k8s/support/logging/
kubectl apply -f k8s/support/tracing/
```

## Security Configuration

### 1. SSL/TLS Setup
```bash
kubectl apply -f k8s/cert-manager/
kubectl apply -f k8s/certificates/
```

### 2. Network Policies
```bash
kubectl apply -f k8s/network-policies/
```

### 3. RBAC Configuration
```bash
kubectl apply -f k8s/rbac/
```

## Monitoring Setup

### 1. Prometheus & Grafana
```bash
helm install prometheus prometheus-community/kube-prometheus-stack \
    --namespace monitoring \
    --create-namespace
```

### 2. ELK Stack
```bash
helm install elasticsearch elastic/elasticsearch
helm install kibana elastic/kibana
helm install filebeat elastic/filebeat
```

### 3. Jaeger
```bash
kubectl apply -f k8s/jaeger/
```

## Maintenance

### Backup Configuration
1. Database backups
2. Configuration backups
3. Application state backups

### Scaling Configuration
1. HPA setup
2. VPA setup
3. Cluster autoscaling

### Monitoring Alerts
1. System health alerts
2. Performance alerts
3. Security alerts

## Troubleshooting

### Common Issues
1. Connection timeouts
2. Memory pressure
3. CPU throttling
4. Network issues

### Debug Commands
```bash
kubectl get pods
kubectl logs <pod-name>
kubectl describe pod <pod-name>
kubectl top pods
kubectl top nodes
```

### Health Checks
1. Endpoint health
2. Database connectivity
3. Cache availability
4. Message queue status
