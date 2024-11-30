import React from 'react';
import { cn } from '@/support/utils/cn';
import { CheckCircleIcon, XCircleIcon } from 'lucide-react';
import { useReservationProcessStore } from '@/stores/reservationProcess.store';

export const ProcessValidation: React.FC = () => {
  const { validationResults } = useReservationProcessStore();

  if (!validationResults.length) {
    return null;
  }

  return (
    <div className="rounded-lg bg-white shadow-sm p-4">
      <h3 className="font-medium text-gray-900">Validation Results</h3>
      
      <div className="mt-2 space-y-2">
        {validationResults.map((result, index) => (
          <div 
            key={index}
            className={cn(
              'p-3 rounded-lg border',
              result.valid 
                ? 'bg-green-50 border-green-200' 
                : 'bg-red-50 border-red-200'
            )}
          >
            <div className="flex items-start gap-2">
              {result.valid ? (
                <CheckCircleIcon className="h-5 w-5 text-green-600 mt-0.5" />
              ) : (
                <XCircleIcon className="h-5 w-5 text-red-600 mt-0.5" />
              )}
              
              <div>
                <p className="font-medium text-sm">
                  {result.rule}
                </p>
                {!result.valid && result.error && (
                  <p className="text-sm text-red-600 mt-1">
                    {result.error}
                  </p>
                )}

                {/* Additional Details */}
                {result.details && (
                  <div className="mt-2 text-xs text-gray-500">
                    <dl className="grid grid-cols-2 gap-1">
                      {Object.entries(result.details).map(([key, value]) => (
                        <React.Fragment key={key}>
                          <dt className="font-medium">{key}:</dt>
                          <dd>{value}</dd>
                        </React.Fragment>
                      ))}
                    </dl>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
