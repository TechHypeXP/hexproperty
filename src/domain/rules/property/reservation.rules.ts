import { ProcessConfiguration, ProcessContext } from '@/types/process';
import { ReservationInput } from '@/domain/process/property/reservation.process';

export const propertyReservationRules: ProcessConfiguration = {
  rules: [
    {
      name: 'MinimumStayRule',
      description: 'Ensures minimum stay duration is met',
      condition: (context: ProcessContext<ReservationInput>) => {
        const { startDate, endDate } = context.input;
        const minStayDays = 2; // Configurable
        const stayDuration = Math.ceil((endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24));
        return stayDuration >= minStayDays;
      },
      error: 'Minimum stay duration not met'
    },
    {
      name: 'AdvanceBookingRule',
      description: 'Ensures booking is made with sufficient notice',
      condition: (context: ProcessContext<ReservationInput>) => {
        const { startDate } = context.input;
        const minAdvanceDays = 1; // Configurable
        const now = new Date();
        const daysInAdvance = Math.ceil((startDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
        return daysInAdvance >= minAdvanceDays;
      },
      error: 'Booking must be made at least 24 hours in advance'
    },
    {
      name: 'MaximumStayRule',
      description: 'Ensures stay duration does not exceed maximum',
      condition: (context: ProcessContext<ReservationInput>) => {
        const { startDate, endDate } = context.input;
        const maxStayDays = 90; // Configurable
        const stayDuration = Math.ceil((endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24));
        return stayDuration <= maxStayDays;
      },
      error: 'Maximum stay duration exceeded'
    }
  ],
  steps: {
    order: [
      'PropertyAvailabilityCheck',
      'TenantVerification',
      'PricingCalculation'
    ],
    conditional: {
      TenantVerification: {
        enabled: true,
        condition: (context: ProcessContext) => {
          // Example: Skip verification for premium tenants
          return !context.state.isPremiumTenant;
        }
      }
    }
  },
  validation: {
    creditScore: {
      minimum: 650,
      preferred: 700
    },
    deposit: {
      percentage: 30,
      minimum: 500
    },
    fees: {
      cleaning: {
        base: 150,
        perDay: 10
      },
      service: {
        percentage: 10
      }
    }
  },
  timing: {
    maxProcessingTime: '1h',
    stepTimeout: '5m'
  }
};
