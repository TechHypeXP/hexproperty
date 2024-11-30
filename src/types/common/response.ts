// Base API response interface
export interface ApiResponse<T> {
  data: T;
  meta?: ResponseMetadata;
  links?: ResponseLinks;
}

// Metadata interface for pagination and other meta information
export interface ResponseMetadata {
  total?: number;
  page?: number;
  pageSize?: number;
  totalPages?: number;
  timestamp?: string;
  requestId?: string;
}

// HATEOAS links
export interface ResponseLinks {
  self?: string;
  first?: string;
  prev?: string;
  next?: string;
  last?: string;
  [key: string]: string | undefined;
}

// Error response interface
export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
  stack?: string;
  timestamp?: string;
  requestId?: string;
}

// Success response type
export type SuccessResponse<T> = {
  success: true;
  data: T;
  meta?: ResponseMetadata;
};

// Error response type
export type ErrorResponse = {
  success: false;
  error: ApiError;
};

// Combined response type
export type ApiResult<T> = SuccessResponse<T> | ErrorResponse;

// Validation error details
export interface ValidationError {
  field: string;
  message: string;
  code: string;
  params?: Record<string, unknown>;
}

// Validation error response
export interface ValidationErrorResponse extends ApiError {
  validationErrors: ValidationError[];
}

// Bulk operation response
export interface BulkOperationResponse<T> {
  successful: Array<{
    id: string;
    data: T;
  }>;
  failed: Array<{
    id: string;
    error: ApiError;
  }>;
  metadata: {
    totalProcessed: number;
    successCount: number;
    failureCount: number;
  };
}

// File upload response
export interface FileUploadResponse {
  fileId: string;
  filename: string;
  mimeType: string;
  size: number;
  url: string;
  metadata?: Record<string, unknown>;
}

// Stream response
export interface StreamResponse<T> {
  data: T;
  isComplete: boolean;
  progress?: number;
  chunk?: number;
  totalChunks?: number;
}
