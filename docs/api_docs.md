# MoMo Transaction API Documentation

## Overview

This REST API exposes access to MoMo SMS transaction data processed via the ETL pipeline.  
It supports full CRUD operations on transaction records.  
All endpoints require API Key authentication with rate limiting protection.

**Base URL (local development):** `http://localhost:8000`  

---
## Security Implementation

### Authentication Method
The API uses a custom API Key authentication system with Base64 encoding for enhanced security.

#### How It Works:
1. **Setup**: On first run, you'll be prompted to set a plain text API key
2. **Storage**: The server stores a Base64 encoded version of your key
3. **Usage**: You send the plain text key in requests; server handles encoding/comparison
4. **Protection**: Rate limiting prevents abuse (1000 requests/minute per IP)

#### Request Headers:
| Header        | Required | Value / Format   |
| ------------- | -------- | ---------------- |
| `X-API-Key`   |        | Your plain text API key |

#### Example (curl):
```bash
curl -H "X-API-Key: your_plain_text_key" http://localhost:8000/transactions
```

#### Error Responses:
- **401 Unauthorized** - Invalid or missing API key
- **429 Too Many Requests** - Rate limit exceeded

### Security Flow:
```
Setup: You type "mysecret123"
|
|-->Server stores: "bXlzZWNyZXQxMjM=" (Base64 encoded)
|    
|-->You send: "mysecret123" in X-API-Key header
|    
|-->Server encodes: "mysecret123" → "bXlzZWNyZXQxMjM="
|   
|-->Server compares: "bXlzZWNyZXQxMjM=" == "bXlzZWNyZXQxMjM="
|
|-->Access Granted
```

---
## Security Usage & Best Practices

### Where Security is Strongly Needed:
- **Production Environments**: Essential for any live deployment
- **Sensitive Data**: Transaction records contain financial information
- **Public Networks**: When API is accessible over internet
- **Multi-user Systems**: When multiple clients access the API

### Recommended Usage:
1. **Key Management**: Store API keys securely, never in client-side code
2. **Key Rotation**: Change API keys periodically in production
3. **HTTPS**: Always use TLS/SSL in production to encrypt traffic
4. **Network Security**: Restrict API access to trusted IP ranges when possible

### Current Limitations:
- **Single Key**: Only one API key supported (no multi-user management)
- **Plain Text Transmission**: Keys sent in plain text (requires HTTPS for security)
- **No Key Expiration**: Keys don't expire automatically
- **Basic Rate Limiting**: Simple IP-based limiting without advanced features

### When to Consider Enhanced Security:
- For multi-tenant applications, implement user-based authentication
- For high-security environments, add JWT tokens or OAuth 2.0
- For compliance requirements, implement key rotation and audit logging
- For public APIs, consider API gateway with advanced rate limiting

---

## Endpoints

## GET /transactions
**Description**: Retrieve a list of all transaction records.

**Method**: GET  
**Path**: `/transactions`

### Request Headers:
| Header        | Required | Value / Format   |
| ------------- | -------- | ---------------- |
| `X-API-Key`   | ✓        | Your plain text API key |

### Response (200 OK):
```json
[
  {
    "TransactionId": 1,
    "Fee": 50,
    "Amount": 1000,
    "balance": 9500,
    "initialBalance": 10000,
    "senderUserId": 123,
    "receiverUserId": 456,
    "transactionDate": "2025-10-01T09:00:00",
    "categoryId": 1,
    "TransactionReference": "REF123456"
  }
]
```

### Error Responses:
- **401 Unauthorized** — Invalid or missing API key
- **429 Too Many Requests** — Rate limit exceeded
- **500 Internal Server Error** — Unexpected error

---

## GET /transactions/{id}
**Description**: Retrieve a single transaction record by its ID.

**Method**: GET  
**Path**: `/transactions/{id}`

### Path Parameter:
| Parameter | Type    | Description           |
| --------- | ------- | --------------------- |
| `id`      | integer | Unique transaction ID |

### Request Headers:
| Header        | Required | Value / Format   |
| ------------- | -------- | ---------------- |
| `X-API-Key`   | ✓        | Your plain text API key |

### Response (200 OK):
```json
{
  "TransactionId": 1,
  "Fee": 50,
  "Amount": 1000,
  "balance": 9500,
  "initialBalance": 10000,
  "senderUserId": 123,
  "receiverUserId": 456,
  "transactionDate": "2025-10-01T09:00:00",
  "categoryId": 1,
  "TransactionReference": "REF123456"
}
```

### Error Responses:
- **401 Unauthorized** — Invalid or missing API key
- **404 Not Found** — Transaction with given ID not found
- **429 Too Many Requests** — Rate limit exceeded
- **500 Internal Server Error** — Unexpected error

---

## POST /transactions
**Description**: Create a new transaction record.

**Method**: POST  
**Path**: `/transactions`

### Request Headers:
| Header        | Required | Value / Format     |
| ------------- | -------- | ------------------ |
| `X-API-Key`   | ✓        | Your plain text API key |
| `Content-Type`| ✓        | `application/json` |

### Request Body (JSON):
```json
{
  "Fee": 50,
  "Amount": 1000,
  "balance": 9500,
  "initialBalance": 10000,
  "senderUserId": 123,
  "receiverUserId": 456,
  "transactionDate": "2025-10-01T09:00:00",
  "categoryId": 1,
  "TransactionReference": "REF123456"
}
```

### Response (201 Created):
```json
{
  "TransactionId": 10,
  "Fee": 50,
  "Amount": 1000,
  "balance": 9500,
  "initialBalance": 10000,
  "senderUserId": 123,
  "receiverUserId": 456,
  "transactionDate": "2025-10-01T09:00:00",
  "categoryId": 1,
  "TransactionReference": "REF123456"
}
```

### Error Responses:
- **400 Bad Request** — Missing or invalid fields
- **401 Unauthorized** — Invalid or missing API key
- **429 Too Many Requests** — Rate limit exceeded
- **500 Internal Server Error** — Unexpected error

---

## PUT /transactions/{id}
**Description**: Update an existing transaction record.

**Method**: PUT  
**Path**: `/transactions/{id}`

### Path Parameter:
| Parameter | Type    | Description                     |
| --------- | ------- | ------------------------------- |
| `id`      | integer | ID of the transaction to update |

### Request Headers:
| Header        | Required | Value / Format     |
| ------------- | -------- | ------------------ |
| `X-API-Key`   | ✓        | Your plain text API key |
| `Content-Type`| ✓        | `application/json` |

### Request Body (JSON):
All fields must be provided:
```json
{
  "Fee": 75,
  "Amount": 1500,
  "balance": 9250,
  "initialBalance": 10000,
  "senderUserId": 123,
  "receiverUserId": 456,
  "transactionDate": "2025-10-01T09:00:00",
  "categoryId": 1,
  "TransactionReference": "REF123456"
}
```

### Response (200 OK):
```json
{
  "TransactionId": 5,
  "Fee": 75,
  "Amount": 1500,
  "balance": 9250,
  "initialBalance": 10000,
  "senderUserId": 123,
  "receiverUserId": 456,
  "transactionDate": "2025-10-01T09:00:00",
  "categoryId": 1,
  "TransactionReference": "REF123456"
}
```

### Error Responses:
- **400 Bad Request** — Invalid data
- **401 Unauthorized** — Invalid or missing API key
- **404 Not Found** — Transaction ID does not exist
- **429 Too Many Requests** — Rate limit exceeded
- **500 Internal Server Error** — Unexpected error

---

## DELETE /transactions/{id}
**Description**: Delete a transaction record.

**Method**: DELETE  
**Path**: `/transactions/{id}`

### Path Parameter:
| Parameter | Type    | Description                     |
| --------- | ------- | ------------------------------- |
| `id`      | integer | ID of the transaction to delete |

### Request Headers:
| Header        | Required | Value / Format   |
| ------------- | -------- | ---------------- |
| `X-API-Key`   | ✓        | Your plain text API key |

### Response (200 OK):
```json
{
  "detail": "Transaction deleted successfully"
}
```

### Error Responses:
- **401 Unauthorized** — Invalid or missing API key
- **404 Not Found** — Transaction ID does not exist
- **429 Too Many Requests** — Rate limit exceeded
- **500 Internal Server Error** — Unexpected error

---

## Notes & Assumptions

- **Timestamps**: All timestamps use ISO 8601 format (e.g., `YYYY-MM-DDTHH:MM:SS`)
- **TransactionId**: Auto-generated by the system; clients should not provide it
- **Required Fields**: `POST /transactions` requires all fields except `TransactionId`
- **Full Updates**: `PUT /transactions/{id}` requires all fields (partial updates not supported)
- **Rate Limiting**: 1000 requests per minute per IP address
- **Security**: API uses custom authentication with Base64 encoding under the hood
- **Evolution**: API logic and requirements may change — ensure documentation stays updated

---

## Getting Started

1. **Start the server**: `python server.py`
2. **Set API key**: Enter your secret key when prompted
3. **Use the key**: Include it in `X-API-Key` header for all requests
4. **Test connectivity**: Use the provided curl example to verify access

**Remember**: Keep your API key secure and not advisory to commit it to version control even if it's decoded!