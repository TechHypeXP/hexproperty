import React from 'react';
import { ProcessContext } from '@/types/process';
import { AlertTriangleIcon, RefreshCwIcon } from 'lucide-react';
import { motion } from 'framer-motion';

interface ProcessErrorProps {
  error: Error;
  context?: ProcessContext;
  onRetry?: () => void;
}

export const ProcessError: React.FC<ProcessErrorProps> = ({
  error,
  context,
  onRetry
}) => {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="bg-red-50 border border-red-200 rounded-lg p-4"
    >
      <div className="flex items-start gap-2">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 300, damping: 20 }}
        >
          <AlertTriangleIcon className="h-5 w-5 text-red-500 mt-0.5" />
        </motion.div>
        
        <div className="flex-1">
          <h3 className="font-medium text-red-800">
            Process Error
          </h3>
          
          <p className="text-sm text-red-600 mt-1">
            {error.message}
          </p>

          {/* Debug Information */}
          {process.env.NODE_ENV === 'development' && (
            <motion.div 
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              transition={{ delay: 0.2 }}
              className="mt-4 space-y-2"
            >
              <h4 className="text-sm font-medium text-red-800">
                Debug Information
              </h4>
              
              <pre className="text-xs bg-red-100 p-2 rounded overflow-auto">
                {JSON.stringify({
                  error: error.message,
                  stack: error.stack,
                  context: {
                    currentStep: context?.currentStep,
                    completedSteps: context?.completedSteps,
                    validationResults: context?.validationResults
                  }
                }, null, 2)}
              </pre>
            </motion.div>
          )}

          {/* Recovery Suggestions */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="mt-4"
          >
            <h4 className="text-sm font-medium text-red-800">
              What can you do?
            </h4>
            <ul className="mt-2 text-sm text-red-600 list-disc list-inside space-y-1">
              <li>Check if all required fields are filled correctly</li>
              <li>Verify your internet connection</li>
              <li>Try refreshing the page</li>
              <li>Contact support if the issue persists</li>
            </ul>
          </motion.div>

          {/* Retry Button */}
          {onRetry && (
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={onRetry}
              className="mt-4 inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-red-700 bg-red-100 rounded-md hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            >
              <RefreshCwIcon className="h-4 w-4" />
              Try Again
            </motion.button>
          )}
        </div>
      </div>
    </motion.div>
  );
};
