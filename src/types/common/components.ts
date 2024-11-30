import { ReactNode } from 'react';

// Base component props
export interface BaseProps {
  className?: string;
  'aria-label'?: string;
  'data-testid'?: string;
}

// Component with children
export interface WithChildren {
  children?: ReactNode;
}

// Loading states
export interface LoadingState {
  isLoading?: boolean;
  loadingText?: string;
}

// Error states
export interface ErrorState {
  error?: Error | null;
  onError?: (error: Error) => void;
}

// Disabled state
export interface DisabledState {
  disabled?: boolean;
  disabledReason?: string;
}

// Common form props
export interface FormProps extends BaseProps {
  onSubmit: (data: unknown) => Promise<void> | void;
  onCancel?: () => void;
  submitLabel?: string;
  cancelLabel?: string;
}

// Common table props
export interface TableProps<T> extends BaseProps {
  data: T[];
  columns: TableColumn<T>[];
  onRowClick?: (item: T) => void;
  sortable?: boolean;
  filterable?: boolean;
}

export interface TableColumn<T> {
  key: keyof T | string;
  header: string;
  render?: (item: T) => ReactNode;
  sortable?: boolean;
  filterable?: boolean;
  width?: number | string;
}

// Common card props
export interface CardProps extends BaseProps, WithChildren {
  title?: string;
  subtitle?: string;
  footer?: ReactNode;
  headerAction?: ReactNode;
}

// Common button props
export interface ButtonProps extends BaseProps, WithChildren, LoadingState, DisabledState {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  icon?: ReactNode;
  iconPosition?: 'left' | 'right';
}

// Common input props
export interface InputProps extends BaseProps, DisabledState {
  name: string;
  label?: string;
  placeholder?: string;
  type?: 'text' | 'number' | 'email' | 'password' | 'tel' | 'url';
  value?: string | number;
  onChange?: (value: string) => void;
  error?: string;
  required?: boolean;
  autoComplete?: string;
}

// Common select props
export interface SelectProps<T> extends BaseProps, DisabledState {
  name: string;
  label?: string;
  options: SelectOption<T>[];
  value?: T;
  onChange?: (value: T) => void;
  error?: string;
  required?: boolean;
  placeholder?: string;
}

export interface SelectOption<T> {
  label: string;
  value: T;
  disabled?: boolean;
}

// Common modal props
export interface ModalProps extends BaseProps, WithChildren {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  closeOnOverlayClick?: boolean;
  closeOnEsc?: boolean;
}

// Common toast props
export interface ToastProps extends BaseProps {
  message: string;
  type?: 'success' | 'error' | 'warning' | 'info';
  duration?: number;
  onClose?: () => void;
}

// Common list props
export interface ListProps<T> extends BaseProps {
  items: T[];
  renderItem: (item: T) => ReactNode;
  keyExtractor: (item: T) => string;
  emptyMessage?: string;
}

// Common grid props
export interface GridProps extends BaseProps, WithChildren {
  columns?: number | { sm?: number; md?: number; lg?: number; xl?: number };
  gap?: number | { x?: number; y?: number };
  alignItems?: 'start' | 'center' | 'end' | 'stretch';
  justifyItems?: 'start' | 'center' | 'end' | 'stretch';
}
