// Base error interface
export interface BaseError extends Error {
  code: string;
  timestamp: string;
  requestId?: string;
  details?: Record<string, unknown>;
}

// Domain error codes
export enum DomainErrorCode {
  // Property related errors
  PropertyNotFound = 'PROPERTY_NOT_FOUND',
  PropertyValidationFailed = 'PROPERTY_VALIDATION_FAILED',
  PropertyAlreadyExists = 'PROPERTY_ALREADY_EXISTS',
  PropertyUnavailable = 'PROPERTY_UNAVAILABLE',
  
  // Tenant related errors
  TenantNotFound = 'TENANT_NOT_FOUND',
  TenantValidationFailed = 'TENANT_VALIDATION_FAILED',
  TenantAlreadyExists = 'TENANT_ALREADY_EXISTS',
  
  // Reservation related errors
  ReservationNotFound = 'RESERVATION_NOT_FOUND',
  ReservationValidationFailed = 'RESERVATION_VALIDATION_FAILED',
  ReservationConflict = 'RESERVATION_CONFLICT',
  
  // Authentication/Authorization errors
  Unauthorized = 'UNAUTHORIZED',
  Forbidden = 'FORBIDDEN',
  InvalidCredentials = 'INVALID_CREDENTIALS',
  TokenExpired = 'TOKEN_EXPIRED',
  
  // Infrastructure errors
  DatabaseError = 'DATABASE_ERROR',
  NetworkError = 'NETWORK_ERROR',
  ExternalServiceError = 'EXTERNAL_SERVICE_ERROR',
  
  // Validation errors
  ValidationError = 'VALIDATION_ERROR',
  InvalidInput = 'INVALID_INPUT',
  
  // Business rule violations
  BusinessRuleViolation = 'BUSINESS_RULE_VIOLATION',
  
  // System errors
  InternalServerError = 'INTERNAL_SERVER_ERROR',
  ServiceUnavailable = 'SERVICE_UNAVAILABLE',
  
  // File operations
  FileNotFound = 'FILE_NOT_FOUND',
  FileUploadFailed = 'FILE_UPLOAD_FAILED',
  InvalidFileType = 'INVALID_FILE_TYPE',
  FileTooLarge = 'FILE_TOO_LARGE'
}

// HTTP error status codes
export enum HttpStatusCode {
  Ok = 200,
  Created = 201,
  NoContent = 204,
  BadRequest = 400,
  Unauthorized = 401,
  Forbidden = 403,
  NotFound = 404,
  Conflict = 409,
  UnprocessableEntity = 422,
  TooManyRequests = 429,
  InternalServerError = 500,
  ServiceUnavailable = 503
}

// Domain error class
export class DomainError extends Error implements BaseError {
  public readonly code: string;
  public readonly timestamp: string;
  public readonly requestId?: string;
  public readonly details?: Record<string, unknown>;
  public readonly httpStatus: HttpStatusCode;

  constructor(params: {
    code: DomainErrorCode;
    message: string;
    httpStatus?: HttpStatusCode;
    details?: Record<string, unknown>;
    requestId?: string;
  }) {
    super(params.message);
    this.name = 'DomainError';
    this.code = params.code;
    this.timestamp = new Date().toISOString();
    this.requestId = params.requestId;
    this.details = params.details;
    this.httpStatus = params.httpStatus || HttpStatusCode.InternalServerError;
  }
}

// Validation error class
export class ValidationError extends DomainError {
  constructor(params: {
    message: string;
    details: Record<string, unknown>;
    requestId?: string;
  }) {
    super({
      code: DomainErrorCode.ValidationError,
      message: params.message,
      httpStatus: HttpStatusCode.UnprocessableEntity,
      details: params.details,
      requestId: params.requestId
    });
    this.name = 'ValidationError';
  }
}

// Authentication error class
export class AuthenticationError extends DomainError {
  constructor(params: {
    code: DomainErrorCode;
    message: string;
    details?: Record<string, unknown>;
    requestId?: string;
  }) {
    super({
      ...params,
      httpStatus: HttpStatusCode.Unauthorized
    });
    this.name = 'AuthenticationError';
  }
}

// Authorization error class
export class AuthorizationError extends DomainError {
  constructor(params: {
    message: string;
    details?: Record<string, unknown>;
    requestId?: string;
  }) {
    super({
      code: DomainErrorCode.Forbidden,
      message: params.message,
      httpStatus: HttpStatusCode.Forbidden,
      details: params.details,
      requestId: params.requestId
    });
    this.name = 'AuthorizationError';
  }
}

// Not found error class
export class NotFoundError extends DomainError {
  constructor(params: {
    code: DomainErrorCode;
    message: string;
    details?: Record<string, unknown>;
    requestId?: string;
  }) {
    super({
      ...params,
      httpStatus: HttpStatusCode.NotFound
    });
    this.name = 'NotFoundError';
  }
}

// Business rule error class
export class BusinessRuleError extends DomainError {
  constructor(params: {
    message: string;
    details?: Record<string, unknown>;
    requestId?: string;
  }) {
    super({
      code: DomainErrorCode.BusinessRuleViolation,
      message: params.message,
      httpStatus: HttpStatusCode.UnprocessableEntity,
      details: params.details,
      requestId: params.requestId
    });
    this.name = 'BusinessRuleError';
  }
}
