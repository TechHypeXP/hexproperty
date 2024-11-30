# HexProperty API Documentation

## Overview
HexProperty provides a comprehensive RESTful API for property management operations. All endpoints use JSON for request and response payloads.

## Authentication
All API requests require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Base URL
```
https://api.hexproperty.com/v1
```

## Property Service API

### Create Property
```http
POST /properties
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Sunset Apartments",
  "address": {
    "street": "123 Main St",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94105"
  },
  "units": [
    {
      "number": "101",
      "type": "2BR",
      "sqft": 1200,
      "rent": 2500
    }
  ],
  "amenities": ["pool", "gym", "parking"]
}
```

### Get Property
```http
GET /properties/{propertyId}
Authorization: Bearer <token>
```

### Update Property
```http
PUT /properties/{propertyId}
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Sunset Luxury Apartments",
  "amenities": ["pool", "gym", "parking", "spa"]
}
```

## Tenant Service API

### Create Tenant
```http
POST /tenants
Content-Type: application/json
Authorization: Bearer <token>

{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "phone": "415-555-0123",
  "documents": {
    "identification": "https://...",
    "proofOfIncome": "https://..."
  }
}
```

### Get Tenant
```http
GET /tenants/{tenantId}
Authorization: Bearer <token>
```

### Update Tenant
```http
PUT /tenants/{tenantId}
Content-Type: application/json
Authorization: Bearer <token>

{
  "phone": "415-555-4567",
  "email": "john.new@example.com"
}
```

## Lease Service API

### Create Lease
```http
POST /leases
Content-Type: application/json
Authorization: Bearer <token>

{
  "propertyId": "prop_123",
  "unitId": "unit_101",
  "tenantId": "tenant_456",
  "terms": {
    "startDate": "2024-01-01",
    "endDate": "2024-12-31",
    "monthlyRent": 2500,
    "securityDeposit": 2500
  },
  "paymentPreferences": {
    "autopay": true,
    "paymentDay": 1
  }
}
```

### Get Lease
```http
GET /leases/{leaseId}
Authorization: Bearer <token>
```

### Update Lease
```http
PUT /leases/{leaseId}
Content-Type: application/json
Authorization: Bearer <token>

{
  "terms": {
    "monthlyRent": 2600
  }
}
```

## Billing Service API

### Create Payment
```http
POST /payments
Content-Type: application/json
Authorization: Bearer <token>

{
  "leaseId": "lease_789",
  "amount": 2500,
  "type": "rent",
  "method": "credit_card",
  "paymentToken": "tok_visa"
}
```

### Get Payment History
```http
GET /payments?leaseId={leaseId}
Authorization: Bearer <token>
```

### Create Invoice
```http
POST /invoices
Content-Type: application/json
Authorization: Bearer <token>

{
  "leaseId": "lease_789",
  "items": [
    {
      "description": "Monthly Rent",
      "amount": 2500
    },
    {
      "description": "Parking Fee",
      "amount": 150
    }
  ],
  "dueDate": "2024-02-01"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Invalid property data",
  "details": {
    "name": "Property name is required"
  }
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Property not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```

## Rate Limiting
- 1000 requests per hour per API key
- Rate limit headers included in response:
  ```
  X-RateLimit-Limit: 1000
  X-RateLimit-Remaining: 999
  X-RateLimit-Reset: 1640995200
  ```

## Pagination
All list endpoints support pagination using:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

Example:
```http
GET /properties?page=2&limit=50
```

Response includes pagination metadata:
```json
{
  "data": [...],
  "pagination": {
    "total": 1250,
    "pages": 25,
    "current": 2,
    "limit": 50
  }
}
```

## Filtering
List endpoints support filtering using query parameters:
```http
GET /properties?city=San Francisco&minRent=2000&maxRent=3000
```

## Sorting
Use `sort` parameter for sorting:
```http
GET /properties?sort=rent:desc,name:asc
```

## Webhooks
Subscribe to events:
```http
POST /webhooks
Content-Type: application/json
Authorization: Bearer <token>

{
  "url": "https://your-server.com/webhook",
  "events": ["lease.created", "payment.received"],
  "secret": "your_webhook_secret"
}
```
