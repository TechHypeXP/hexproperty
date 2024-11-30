# HexProperty Serverless Deployment Guide (Staging)

## Overview
This guide details the deployment of HexProperty using GCP Cloud Run and Cloud Functions for staging environment, optimized for low concurrency (max 5-6 concurrent requests).

## Infrastructure Components

### Cloud Run Services
| Service | Min Instances | Max Instances | Memory | CPU | Max Concurrency |
|---------|---------------|---------------|---------|-----|-----------------|
| Frontend | 0 | 2 | 256Mi | 0.5 | 6 |
| Property-API | 0 | 2 | 256Mi | 0.5 | 6 |
| Tenant-API | 0 | 2 | 256Mi | 0.5 | 6 |
| Lease-API | 0 | 2 | 256Mi | 0.5 | 6 |
| Billing-API | 0 | 2 | 256Mi | 0.5 | 6 |

### Cloud Functions
| Function | Memory | Timeout | Type | Trigger |
|----------|---------|----------|------|---------|
| property-events | 256MB | 60s | Event | Pub/Sub |
| tenant-events | 256MB | 60s | Event | Pub/Sub |
| lease-processor | 256MB | 120s | Event | Pub/Sub |
| payment-processor | 512MB | 120s | Event | Pub/Sub |
| document-generator | 512MB | 180s | HTTP | HTTP |

### Managed Services
| Service | Type | Tier | Size |
|---------|------|------|------|
| Cloud SQL | PostgreSQL | db-f1-micro | 10GB |
| Memorystore | Redis | Basic | 1GB |
| Cloud Storage | Standard | - | Pay per use |
| Pub/Sub | Standard | - | Pay per use |

## Deployment Configurations

### Frontend Service (Cloud Run)
```yaml
service: frontend
runtime: nodejs16
instance_class: F1

automatic_scaling:
  min_instances: 0
  max_instances: 2
  target_cpu_utilization: 0.7
  max_concurrent_requests: 6

resources:
  cpu: 0.5
  memory_gb: 0.25
  disk_size_gb: 10

env_variables:
  NODE_ENV: "staging"
  API_URL: "https://api-staging.hexproperty.com"
```

### Backend API Services (Cloud Run)
```yaml
service: [service-name]-api
runtime: nodejs16
instance_class: F1

automatic_scaling:
  min_instances: 0
  max_instances: 2
  target_cpu_utilization: 0.7
  max_concurrent_requests: 6

resources:
  cpu: 0.5
  memory_gb: 0.25
  disk_size_gb: 10

env_variables:
  NODE_ENV: "staging"
  DB_SOCKET: "/cloudsql/[instance-connection-name]"
  REDIS_URL: "redis://10.0.0.1:6379"
```

### Event Processing Functions
```yaml
runtime: nodejs16
entry_point: processEvent
memory: 256MB
timeout: 60s
environment_variables:
  NODE_ENV: "staging"
```

## Cost Estimation (Monthly)

### Cloud Run Costs
| Service | Requests/Month | Compute Time | Est. Cost |
|---------|---------------|--------------|-----------|
| Frontend | 5000 | 25h | $3-5 |
| Each API | 3000 | 15h | $2-4 |
Total Cloud Run: $15-25/month

### Cloud Functions Costs
| Type | Invocations | Compute Time | Est. Cost |
|------|-------------|--------------|-----------|
| Event Processing | 2000 | 10h | $1-2 |
| HTTP Functions | 1000 | 5h | $1-2 |
Total Functions: $5-10/month

### Managed Services Costs
| Service | Configuration | Est. Cost |
|---------|--------------|-----------|
| Cloud SQL | db-f1-micro | $7.50 |
| Memorystore | Basic 1GB | $8.50 |
| Cloud Storage | < 1GB | $0.50 |
| Pub/Sub | Basic usage | $1-2 |
Total Services: $17-20/month

**Total Estimated Monthly Cost: $37-55**

## Deployment Steps

### 1. Initial Setup
```bash
# Set project and region
gcloud config set project hexproperty-staging
gcloud config set run/region us-central1
gcloud config set functions/region us-central1
```

### 2. Database Setup
```bash
# Create Cloud SQL instance
gcloud sql instances create hexproperty-staging \
  --database-version=POSTGRES_13 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --storage-size=10GB
```

### 3. Redis Setup
```bash
# Create Memorystore instance
gcloud redis instances create hexproperty-cache \
  --size=1 \
  --region=us-central1 \
  --tier=basic
```

### 4. Deploy Cloud Run Services
```bash
# Frontend
gcloud run deploy frontend \
  --source ./frontend \
  --platform managed \
  --memory 256Mi \
  --cpu 0.5 \
  --max-instances 2 \
  --concurrency 6

# Backend APIs
gcloud run deploy property-api \
  --source ./services/property \
  --platform managed \
  --memory 256Mi \
  --cpu 0.5 \
  --max-instances 2 \
  --concurrency 6
```

### 5. Deploy Cloud Functions
```bash
# Event processor
gcloud functions deploy property-events \
  --runtime nodejs16 \
  --trigger-topic property-events \
  --memory 256MB \
  --timeout 60s
```

## Monitoring Setup

### Cloud Run Metrics
- Request count
- Request latency
- Container instance count
- Memory utilization
- CPU utilization

### Cloud Functions Metrics
- Execution count
- Execution time
- Memory usage
- Error count

### Alerts
```yaml
# CPU Usage Alert
metric: run.googleapis.com/container/cpu_utilization
threshold: 0.7
duration: 5m
notification: email

# Memory Usage Alert
metric: run.googleapis.com/container/memory_utilization
threshold: 0.8
duration: 5m
notification: email
```

## Scaling Considerations

### Cloud Run
- Services start with 0 instances (cold start acceptable for staging)
- Max 2 instances per service to control costs
- Max 6 concurrent requests per instance
- CPU target utilization at 70%

### Cloud Functions
- No minimum instances
- Concurrent executions limited to 1-2
- Memory optimized for cold start performance
- Timeout values based on operation complexity

## Security Configuration

### Service Authentication
```yaml
# Cloud Run IAM
service-account: staging-runtime@hexproperty-staging.iam.gserviceaccount.com
roles:
  - roles/run.invoker
  - roles/cloudsql.client

# Cloud Functions IAM
service-account: staging-functions@hexproperty-staging.iam.gserviceaccount.com
roles:
  - roles/cloudfunctions.invoker
  - roles/pubsub.publisher
```

### Network Security
- Private Cloud SQL connection
- VPC connector for Redis access
- Cloud Armor basic protection

## Backup Configuration

### Database
- Daily automated backups
- 7-day retention
- Point-in-time recovery enabled

### Application Data
- Cloud Storage versioning enabled
- 30-day object versioning
- Cross-region replication disabled for staging

## Maintenance Procedures

### Regular Tasks
1. Monitor cold start frequency
2. Review error rates
3. Analyze cost distribution
4. Check resource utilization

### Monthly Review
1. Performance metrics analysis
2. Cost optimization opportunities
3. Security patch status
4. Backup verification

## Troubleshooting

### Common Issues
1. Cold Start Latency
   - Solution: Adjust minimum instances if needed
   
2. Memory Errors
   - Solution: Review memory allocation and garbage collection

3. Connection Timeouts
   - Solution: Check connection pooling and timeout settings

4. Cost Spikes
   - Solution: Review max instances and concurrency settings
