import { create } from 'zustand';
import { ProcessContext, ValidationResult } from '@/types/process';

interface ReservationProcessState {
  currentStep: string | null;
  processContext: ProcessContext | null;
  validationResults: ValidationResult[];
  stepProgress: number | null;
  error: Error | null;
  
  // Actions
  setStep: (step: string) => void;
  updateContext: (context: Partial<ProcessContext>) => void;
  setStepProgress: (progress: number) => void;
  addValidationResult: (result: ValidationResult) => void;
  setError: (error: Error | null) => void;
  resetProcess: () => void;
}

export const useReservationProcessStore = create<ReservationProcessState>((set) => ({
  currentStep: null,
  processContext: null,
  validationResults: [],
  stepProgress: null,
  error: null,

  setStep: (step) => set({ 
    currentStep: step,
    stepProgress: 0 // Reset progress when step changes
  }),

  updateContext: (context) => set((state) => ({ 
    processContext: state.processContext ? {
      ...state.processContext,
      ...context
    } : context
  })),

  setStepProgress: (progress) => set({ 
    stepProgress: progress 
  }),

  addValidationResult: (result) => set((state) => ({
    validationResults: [...state.validationResults, result]
  })),

  setError: (error) => set({ error }),

  resetProcess: () => set({ 
    currentStep: null,
    processContext: null,
    validationResults: [],
    stepProgress: null,
    error: null
  })
}));
