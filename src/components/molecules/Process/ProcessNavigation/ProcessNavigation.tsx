import React from 'react';
import { Button } from '@/interface/components/atoms/Button';
import { ArrowLeftIcon, ArrowRightIcon } from 'lucide-react';

interface ProcessNavigationProps {
  canProceed?: boolean;
  onNext?: () => void;
  onBack?: () => void;
}

export const ProcessNavigation: React.FC<ProcessNavigationProps> = ({
  canProceed,
  onNext,
  onBack
}) => {
  return (
    <div className="flex justify-between items-center pt-4 border-t">
      <Button
        variant="outline"
        onClick={onBack}
        className="flex items-center gap-2"
      >
        <ArrowLeftIcon className="h-4 w-4" />
        Back
      </Button>

      <Button
        onClick={onNext}
        disabled={!canProceed}
        className="flex items-center gap-2"
      >
        Next
        <ArrowRightIcon className="h-4 w-4" />
      </Button>
    </div>
  );
};
