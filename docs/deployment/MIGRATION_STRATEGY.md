# HexProperty Zero-Downtime Migration Strategy

## Migration Paths

### Serverless to Kubernetes Migration

#### Phase 1: Parallel Infrastructure Setup (Week 1-2)
1. **Infrastructure Preparation**
   ```bash
   # Set up GKE cluster alongside existing Cloud Run
   gcloud container clusters create hexproperty-prod \
     --num-nodes=3 \
     --machine-type=e2-standard-2 \
     --region=us-central1 \
     --enable-autoscaling \
     --min-nodes=3 \
     --max-nodes=6
   ```

2. **Database Migration Strategy**
   - Create read replica of Cloud SQL
   - Promote to primary when ready
   - Zero downtime using Cloud SQL failover
   ```sql
   -- Enable high availability
   gcloud sql instances patch hexproperty-prod \
     --availability-type REGIONAL
   ```

3. **DNS and Load Balancing**
   ```yaml
   # Cloud Load Balancer Configuration
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: hexproperty-ingress
     annotations:
       kubernetes.io/ingress.global-static-ip-name: "hexproperty-ip"
   spec:
     rules:
     - host: api.hexproperty.com
       http:
         paths:
         - path: /*
           backend:
             service:
               name: backend-svc
               port:
                 number: 80
   ```

#### Phase 2: Service Migration (Week 2-3)
1. **Traffic Migration Strategy**
   ```yaml
   # Cloud Run Traffic Split
   steps:
   - name: 'gcr.io/cloud-builders/gcloud'
     args:
     - run
     - services
     - update-traffic
     - frontend
     - --to-revisions=LATEST=95,previous=5
   ```

2. **Kubernetes Deployment**
   ```yaml
   # Progressive rollout
   spec:
     strategy:
       type: RollingUpdate
       rollingUpdate:
         maxSurge: 1
         maxUnavailable: 0
   ```

3. **Health Check Configuration**
   ```yaml
   livenessProbe:
     httpGet:
       path: /health
       port: 8080
     initialDelaySeconds: 30
     periodSeconds: 10
   readinessProbe:
     httpGet:
       path: /ready
       port: 8080
     initialDelaySeconds: 5
     periodSeconds: 5
   ```

#### Phase 3: Validation and Cutover (Week 3-4)
1. **Monitoring and Validation**
   ```yaml
   # Prometheus monitoring
   apiVersion: monitoring.coreos.com/v1
   kind: ServiceMonitor
   metadata:
     name: api-monitor
   spec:
     endpoints:
     - interval: 15s
       path: /metrics
   ```

2. **Rollback Plan**
   ```bash
   # Quick rollback to Cloud Run
   gcloud run services update-traffic frontend \
     --to-revisions=previous=100
   ```

### Zero-Downtime Guarantees

#### 1. Database Continuity
```sql
-- Create read replica
gcloud sql instances create hexproperty-replica \
  --master-instance-name=hexproperty-prod \
  --region=us-central1

-- Promote replica (zero downtime)
gcloud sql instances promote-replica hexproperty-replica
```

#### 2. Traffic Management
```yaml
# Progressive traffic shift
apiVersion: networking.gcp.k8s.io/v1
kind: MultiClusterIngress
metadata:
  name: hexproperty-ingress
spec:
  template:
    spec:
      backend:
        serviceName: frontend-svc
        servicePort: 80
  clusters:
  - name: cluster-1
    weight: 90
  - name: cluster-2
    weight: 10
```

#### 3. State Management
```yaml
# Session persistence
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
data:
  redis.conf: |
    maxmemory 2gb
    maxmemory-policy allkeys-lru
```

## Monitoring During Migration

### 1. Key Metrics
```yaml
# Prometheus Alert Rules
groups:
- name: migration
  rules:
  - alert: HighLatency
    expr: http_request_duration_seconds > 2
    for: 5m
  - alert: ErrorSpike
    expr: error_rate > 0.01
    for: 2m
```

### 2. Performance Tracking
```yaml
# Grafana Dashboard
dashboard:
  panels:
    - title: "Migration Progress"
      type: graph
      targets:
        - expr: sum(rate(http_requests_total[5m])) by (backend)
```

## Automated Rollback Triggers

### 1. Error Rate Threshold
```yaml
# Rollback Automation
triggers:
  - metric: error_rate
    threshold: 0.05
    duration: 2m
    action: rollback
```

### 2. Latency Threshold
```yaml
triggers:
  - metric: p95_latency
    threshold: 1000ms
    duration: 5m
    action: rollback
```

## Cost Management During Migration

### 1. Resource Overlap Period
- Dual-running costs: ~20-30% increase
- Duration: 2-4 weeks
- Optimization strategy:
  ```yaml
  # Resource limits during migration
  resources:
    requests:
      cpu: 200m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi
  ```

### 2. Cost Monitoring
```yaml
# Budget alert configuration
budget:
  amount: 1000
  alerts:
    - threshold: 0.8
      notification: email
```

## Security Considerations

### 1. Secret Management
```yaml
# Secret rotation during migration
apiVersion: secretmanager.cnrm.cloud.google.com/v1beta1
kind: SecretManagerSecret
metadata:
  name: api-key
spec:
  replication:
    automatic: true
```

### 2. Network Security
```yaml
# Network policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
spec:
  podSelector:
    matchLabels:
      app: api
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
```

## Validation Checklist

### Pre-Migration
- [ ] Database backup verified
- [ ] DNS TTL lowered
- [ ] Monitoring in place
- [ ] Load testing completed
- [ ] Rollback plan tested

### During Migration
- [ ] Error rates normal
- [ ] Latency within SLA
- [ ] Database replication lag < 1s
- [ ] Zero dropped connections
- [ ] Session persistence verified

### Post-Migration
- [ ] All traffic migrated
- [ ] Performance metrics stable
- [ ] Backup systems verified
- [ ] Old system archived
- [ ] Documentation updated

## Emergency Procedures

### 1. Instant Rollback
```bash
# Immediate traffic shift
gcloud run services update-traffic frontend \
  --to-revisions=previous=100

# Kubernetes cleanup
kubectl delete -f k8s/
```

### 2. Data Consistency
```sql
-- Verify data consistency
SELECT COUNT(*) FROM audit_log
WHERE timestamp > migration_start
  AND status = 'error';
```

### 3. Communication Plan
- Status page updates
- Customer notification
- Internal alerts
- Stakeholder updates
