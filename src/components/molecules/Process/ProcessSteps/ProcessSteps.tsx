import React from 'react';
import { cn } from '@/support/utils/cn';
import { ProcessContext } from '@/types/process';
import { CheckCircleIcon, ArrowRightCircleIcon, CircleIcon } from 'lucide-react';
import { motion } from 'framer-motion';

interface ProcessStep {
  name: string;
  description: string;
  validation?: Record<string, any>;
}

interface ProcessStepsProps {
  steps: ProcessStep[];
  currentStep?: string;
  context?: ProcessContext;
}

export const ProcessSteps: React.FC<ProcessStepsProps> = ({
  steps,
  currentStep,
  context
}) => {
  return (
    <div className="flex flex-col md:flex-row gap-4">
      {steps.map((step, index) => {
        const isCompleted = context?.completedSteps?.includes(step.name);
        const isCurrent = currentStep === step.name;
        
        return (
          <motion.div 
            key={step.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className={cn(
              'p-4 rounded-lg border flex-1',
              isCompleted && 'bg-green-50 border-green-200',
              isCurrent && 'bg-blue-50 border-blue-200',
              !isCompleted && !isCurrent && 'bg-gray-50'
            )}
          >
            <div className="flex items-center gap-2">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", stiffness: 300, damping: 20 }}
              >
                {isCompleted ? (
                  <CheckCircleIcon className="h-5 w-5 text-green-500" />
                ) : isCurrent ? (
                  <ArrowRightCircleIcon className="h-5 w-5 text-blue-500" />
                ) : (
                  <CircleIcon className="h-5 w-5 text-gray-400" />
                )}
              </motion.div>
              <span className="font-medium">{step.name}</span>
            </div>
            
            <p className="mt-1 text-sm text-gray-600">
              {step.description}
            </p>

            {/* Step Progress */}
            {isCurrent && context?.stepProgress && (
              <motion.div 
                className="mt-2"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
              >
                <div className="h-1 bg-gray-200 rounded-full overflow-hidden">
                  <motion.div 
                    className="h-full bg-blue-500 rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${context.stepProgress}%` }}
                    transition={{ duration: 0.5, ease: "easeOut" }}
                  />
                </div>
                <motion.p 
                  className="mt-1 text-xs text-blue-600 text-right"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.3 }}
                >
                  {context.stepProgress}% Complete
                </motion.p>
              </motion.div>
            )}
          </motion.div>
        );
      })}
    </div>
  );
};
