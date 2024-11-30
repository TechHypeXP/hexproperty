import React from 'react';
import { cn } from '@/support/utils/cn';
import { CheckCircleIcon, ArrowRightCircleIcon } from 'lucide-react';
import { useReservationProcessStore } from '@/stores/reservationProcess.store';
import { Progress } from '@/interface/components/atoms/Progress';

export const ProcessStatus: React.FC = () => {
  const { processContext, stepProgress } = useReservationProcessStore();

  if (!processContext) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg shadow-sm p-4">
      <h3 className="font-medium text-gray-900">Process Status</h3>
      
      <div className="mt-2 space-y-2">
        {/* Completed Steps */}
        {processContext.completedSteps?.map(step => (
          <div 
            key={step}
            className="flex items-center gap-2 p-2 rounded-md bg-green-50"
          >
            <CheckCircleIcon className="h-5 w-5 text-green-500" />
            <span className="text-sm font-medium text-green-700">
              {step}
            </span>
          </div>
        ))}

        {/* Current Step */}
        {processContext.currentStep && (
          <div className="p-2 rounded-md bg-blue-50">
            <div className="flex items-center gap-2">
              <ArrowRightCircleIcon className="h-5 w-5 text-blue-500" />
              <span className="text-sm font-medium text-blue-700">
                {processContext.currentStep}
              </span>
            </div>

            {/* Progress Bar */}
            {typeof stepProgress === 'number' && (
              <div className="mt-2">
                <Progress 
                  value={stepProgress} 
                  className="h-1"
                />
                <p className="mt-1 text-xs text-blue-600 text-right">
                  {stepProgress}% Complete
                </p>
              </div>
            )}
          </div>
        )}

        {/* Next Steps */}
        {processContext.remainingSteps?.map(step => (
          <div 
            key={step}
            className="flex items-center gap-2 p-2 text-gray-500"
          >
            <div className="h-5 w-5 rounded-full border-2 border-gray-300" />
            <span className="text-sm">
              {step}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
