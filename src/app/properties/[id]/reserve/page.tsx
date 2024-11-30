import React from 'react';
import { ReservationFlow } from '@/interface/components/organisms/ReservationFlow/ReservationFlow';

interface ReservationPageProps {
  params: {
    id: string;
  };
}

export default function ReservationPage({ params }: ReservationPageProps) {
  return (
    <div className="container mx-auto py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold mb-6">
          Reserve Property
        </h1>
        
        <ReservationFlow 
          propertyId={params.id}
          onComplete={(result) => {
            if (result.success) {
              // Redirect to confirmation page
              window.location.href = `/properties/${params.id}/reserve/confirmation?id=${result.reservationId}`;
            }
          }}
        />
      </div>
    </div>
  );
}
