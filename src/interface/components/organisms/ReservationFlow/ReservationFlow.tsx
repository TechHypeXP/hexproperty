import React, { useEffect } from 'react';
import { useMutation } from '@tanstack/react-query';
import { ProcessContext } from '@/types/process';
import { PropertyReservationProcess } from '@/domain/process/property/reservation.process';
import { ProcessSteps } from '../../molecules/ProcessSteps/ProcessSteps';
import { ProcessStatus } from '../../molecules/ProcessStatus/ProcessStatus';
import { ProcessError } from '../../molecules/ProcessError/ProcessError';
import { ProcessValidation } from '../../molecules/ProcessValidation/ProcessValidation';
import { ProcessNavigation } from '../../molecules/ProcessNavigation/ProcessNavigation';
import { ReservationForm } from '../../molecules/ReservationForm/ReservationForm';
import { propertyReservationRules } from '@/domain/rules/property/reservation.rules';
import { useServices } from '@/support/di/hooks/useServices';
import { PropertyService } from '@/domain/services/property.service';
import { TenantService } from '@/domain/services/tenant.service';
import { DocumentService } from '@/domain/services/document.service';
import { useReservationProcessStore } from '@/stores/reservationProcess.store';
import { motion, AnimatePresence } from 'framer-motion';

export interface ReservationResult {
  success: boolean;
  reservationId?: string;
  error?: Error;
  context: ProcessContext;
}

interface ReservationInput {
  propertyId: string;
  startDate: Date;
  endDate: Date;
  tenantId: string;
}

interface ReservationFlowProps {
  propertyId: string;
  onComplete?: (result: ReservationResult) => void;
}

export const ReservationFlow: React.FC<ReservationFlowProps> = ({
  propertyId,
  onComplete
}) => {
  const { 
    currentStep, 
    processContext, 
    setStep, 
    updateContext,
    setStepProgress,
    addValidationResult,
    setError,
    resetProcess
  } = useReservationProcessStore();

  // Get services through DI
  const { propertyService, tenantService, documentService } = useServices({
    propertyService: PropertyService,
    tenantService: TenantService,
    documentService: DocumentService
  });

  // Reset process state on unmount
  useEffect(() => {
    return () => resetProcess();
  }, [resetProcess]);

  // Use our reservation process
  const reservationMutation = useMutation({
    mutationFn: async (input: ReservationInput) => {
      try {
        const process = new PropertyReservationProcess(
          propertyService,
          tenantService,
          documentService
        );
        
        // Subscribe to process updates
        process.onStepChange((step) => {
          setStep(step);
        });

        process.onContextUpdate((ctx) => {
          updateContext(ctx);
        });

        process.onStepProgress((progress) => {
          setStepProgress(progress);
        });

        process.onValidation((result) => {
          addValidationResult(result);
        });
        
        const result = await process.execute(input);
        return result;
      } catch (error) {
        setError(error as Error);
        throw error;
      }
    },
    onSuccess: (result) => {
      onComplete?.(result);
    }
  });

  return (
    <div className="space-y-6">
      {/* Process Steps Visualization */}
      <AnimatePresence mode="wait">
        <motion.div
          key="steps"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
        >
          <ProcessSteps 
            steps={propertyReservationRules.steps}
            currentStep={currentStep}
            context={processContext}
          />
        </motion.div>
      </AnimatePresence>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <AnimatePresence mode="wait">
          <motion.div
            key="form"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
          >
            {/* Reservation Form */} 
            <ReservationForm
              propertyId={propertyId}
              onSubmit={data => reservationMutation.mutate(data)}
              isLoading={reservationMutation.isPending}
            />
          </motion.div>
        </AnimatePresence>

        <div className="space-y-4">
          <AnimatePresence mode="wait">
            {/* Process Status & Validation */}
            {processContext && (
              <motion.div
                key="status"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-4"
              >
                <ProcessStatus />
                <ProcessValidation />
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {/* Navigation Controls */}
      <AnimatePresence mode="wait">
        <motion.div
          key="navigation"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
        >
          <ProcessNavigation 
            canProceed={processContext?.canProceedToNextStep}
            onNext={() => {
              if (processContext?.nextStep) {
                setStep(processContext.nextStep);
              }
            }}
            onBack={() => {
              if (processContext?.previousStep) {
                setStep(processContext.previousStep);
              }
            }}
          />
        </motion.div>
      </AnimatePresence>

      {/* Error Display */}
      <AnimatePresence mode="wait">
        {reservationMutation.error && (
          <motion.div
            key="error"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
          >
            <ProcessError 
              error={reservationMutation.error as Error}
              context={processContext}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
