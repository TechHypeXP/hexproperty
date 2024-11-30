---
title: HexProperty Architecture Overview v1.7 -- 2024-11-27
---

> Wednesday, November 27, 2024 12:45 PM

[Previous content remains the same until tech stack section]

# Tech Stack:

## Microservices Layer:
- Primary: Google Cloud Run
- Secondary: Kong

## Application Layer:
- Primary: Google Cloud Functions
- Secondary: FastAPI

## Event Infrastructure Layer:
- Primary: Google Cloud Pub/Sub
- Secondary: Apache Kafka

## Data Infrastructure Layer:
- Primary: Google Cloud Bigtable
- Secondary: Gino

## Support Infrastructure Layer:
- Primary: Google Stackdriver
- Secondary: Prometheus

## Interface Layer:
- Primary: Google Cloud API Gateway
- Secondary: Kong

## Service Mesh Layer:
- Primary: Google Cloud Service Mesh (Istio)
- Secondary: Linkerd

## Error Tracking:
- Primary: Sentry
- Secondary: Google Cloud Operations Suite

## Performance Monitoring:
- Primary: Google Cloud Operations Suite
- Secondary: Grafana + Prometheus

## Documentation:
- TypeDoc for TypeScript code documentation
- GraphiQL (or GraphQL Playground) for GraphQL API documentation
- Docusaurus for comprehensive project documentation

[Rest of the document remains the same]

## Version History
- v1.7 (2024-11-27): Updated tech stack to include complete primary/secondary options for all monitoring aspects
- v1.6 (2024-11-20): Initial comprehensive architecture documentation
