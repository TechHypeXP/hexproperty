// Pagination request parameters
export interface PaginationParams {
  page?: number;
  pageSize?: number;
  cursor?: string;
}

// Sorting parameters
export interface SortParams {
  field: string;
  direction: 'asc' | 'desc';
}

// Filtering parameters
export interface FilterParams {
  field: string;
  operator: FilterOperator;
  value: unknown;
}

// Filter operators
export enum FilterOperator {
  Equals = 'eq',
  NotEquals = 'neq',
  GreaterThan = 'gt',
  GreaterThanOrEqual = 'gte',
  LessThan = 'lt',
  LessThanOrEqual = 'lte',
  Contains = 'contains',
  StartsWith = 'startsWith',
  EndsWith = 'endsWith',
  In = 'in',
  NotIn = 'notIn',
  Between = 'between',
  IsNull = 'isNull',
  IsNotNull = 'isNotNull'
}

// Combined query parameters
export interface QueryParams {
  pagination?: PaginationParams;
  sort?: SortParams[];
  filters?: FilterParams[];
  search?: string;
  include?: string[];
}

// Paginated response
export interface PaginatedResponse<T> {
  items: T[];
  meta: {
    total: number;
    page: number;
    pageSize: number;
    totalPages: number;
    hasNextPage: boolean;
    hasPreviousPage: boolean;
    nextCursor?: string;
  };
}

// Cursor-based pagination
export interface CursorPaginationParams {
  first?: number;
  after?: string;
  last?: number;
  before?: string;
}

// Edge type for cursor-based pagination
export interface Edge<T> {
  node: T;
  cursor: string;
}

// Connection type for cursor-based pagination (Relay-style)
export interface Connection<T> {
  edges: Edge<T>[];
  pageInfo: {
    hasNextPage: boolean;
    hasPreviousPage: boolean;
    startCursor?: string;
    endCursor?: string;
  };
  totalCount: number;
}

// Infinite scroll pagination
export interface InfiniteScrollParams {
  limit: number;
  offset: number;
}

// Virtual pagination for large datasets
export interface VirtualPaginationParams {
  startIndex: number;
  endIndex: number;
  bufferSize?: number;
}
