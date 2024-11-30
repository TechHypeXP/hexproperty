import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { format } from 'date-fns';
import { useQuery } from '@tanstack/react-query';
import { useServices } from '@/support/di/hooks/useServices';
import { PropertyService } from '@/domain/services/property.service';
import { TenantService } from '@/domain/services/tenant.service';
import { Button } from '@/interface/components/atoms/Button';
import { Input } from '@/interface/components/atoms/Input';
import { DatePicker } from '@/interface/components/atoms/DatePicker';

const reservationSchema = z.object({
  propertyId: z.string(),
  startDate: z.date(),
  endDate: z.date(),
  tenantId: z.string()
});

type ReservationFormData = z.infer<typeof reservationSchema>;

interface ReservationFormProps {
  propertyId: string;
  onSubmit: (data: ReservationFormData) => void;
  isLoading?: boolean;
}

export const ReservationForm: React.FC<ReservationFormProps> = ({
  propertyId,
  onSubmit,
  isLoading
}) => {
  const { propertyService, tenantService } = useServices({
    propertyService: PropertyService,
    tenantService: TenantService
  });

  // Get property details
  const { data: property } = useQuery({
    queryKey: ['property', propertyId],
    queryFn: () => propertyService.getProperty(propertyId)
  });

  const form = useForm<ReservationFormData>({
    resolver: zodResolver(reservationSchema),
    defaultValues: {
      propertyId,
      startDate: new Date(),
      endDate: new Date(),
      tenantId: '' // In a real app, this would be the current user's ID
    }
  });

  const handleSubmit = form.handleSubmit((data) => {
    onSubmit(data);
  });

  if (!property) {
    return <div>Loading property details...</div>;
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium mb-4">
          Reserve {property.name}
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Start Date */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Check-in Date
            </label>
            <DatePicker
              selected={form.watch('startDate')}
              onChange={(date) => form.setValue('startDate', date)}
              minDate={new Date()}
              placeholderText="Select check-in date"
              className="w-full"
            />
            {form.formState.errors.startDate && (
              <p className="mt-1 text-sm text-red-600">
                {form.formState.errors.startDate.message}
              </p>
            )}
          </div>

          {/* End Date */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Check-out Date
            </label>
            <DatePicker
              selected={form.watch('endDate')}
              onChange={(date) => form.setValue('endDate', date)}
              minDate={form.watch('startDate')}
              placeholderText="Select check-out date"
              className="w-full"
            />
            {form.formState.errors.endDate && (
              <p className="mt-1 text-sm text-red-600">
                {form.formState.errors.endDate.message}
              </p>
            )}
          </div>
        </div>

        {/* Property Details */}
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <h4 className="font-medium mb-2">Property Details</h4>
          <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <dt className="text-sm text-gray-500">Monthly Rent</dt>
              <dd className="text-sm font-medium">
                ${property.monthlyRent.toLocaleString()}
              </dd>
            </div>
            <div>
              <dt className="text-sm text-gray-500">Status</dt>
              <dd className="text-sm font-medium">
                {property.status}
              </dd>
            </div>
            <div>
              <dt className="text-sm text-gray-500">Location</dt>
              <dd className="text-sm font-medium">
                {property.location}
              </dd>
            </div>
          </dl>
        </div>

        {/* Submit Button */}
        <div className="mt-6">
          <Button
            type="submit"
            disabled={isLoading}
            className="w-full"
          >
            {isLoading ? 'Processing...' : 'Reserve Property'}
          </Button>
        </div>
      </div>
    </form>
  );
};
