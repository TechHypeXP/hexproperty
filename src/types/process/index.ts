import { ValidationResult } from '../common/validation';

export interface ProcessContext<T = any> {
  input: T;
  state: Record<string, any>;
  metadata: ProcessMetadata;
}

export interface ProcessMetadata {
  processId: string;
  startedAt: Date;
  currentStep?: string;
  completedSteps: string[];
}

export interface ProcessResult<T> {
  success: boolean;
  data?: T;
  error?: Error;
  context: ProcessContext;
}

export interface BusinessProcessStep<TContext extends ProcessContext = ProcessContext> {
  name: string;
  description: string;
  required: boolean;
  condition?: (context: TContext) => boolean | Promise<boolean>;
  execute: (context: TContext) => Promise<ProcessResult<any>>;
}

export interface BusinessProcess<TInput, TOutput> {
  name: string;
  description: string;
  steps: BusinessProcessStep[];
  validate: (input: TInput) => Promise<ValidationResult>;
  execute: (input: TInput) => Promise<ProcessResult<TOutput>>;
}

export interface BusinessRule {
  name: string;
  description: string;
  condition: (context: ProcessContext) => boolean | Promise<boolean>;
  error?: string;
}

export interface ProcessConfiguration {
  rules: BusinessRule[];
  steps: {
    order: string[];
    conditional: Record<string, {
      enabled: boolean;
      condition?: (context: ProcessContext) => boolean;
    }>;
  };
  validation: Record<string, any>;
  timing: {
    maxProcessingTime?: string;
    stepTimeout?: string;
  };
}
