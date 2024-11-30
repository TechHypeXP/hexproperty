import { 
  BusinessProcess,
  ProcessContext,
  ProcessResult,
  ValidationResult 
} from '@/types/process';
import { PropertyId, TenantId } from '@/domain/models/property/property';
import { PropertyService } from '@/domain/services/property.service';
import { TenantService } from '@/domain/services/tenant.service';
import { DocumentService } from '@/domain/services/document.service';
import { Injectable } from '@/support/di/decorators';
import { PropertyNotAvailableError } from '@/domain/errors/property.errors';

// Input/Output types
export interface ReservationInput {
  propertyId: PropertyId;
  tenantId: TenantId;
  startDate: Date;
  endDate: Date;
  additionalRequests?: string;
  documents?: string[];
}

export interface ReservationOutput {
  reservationId: string;
  status: 'CONFIRMED' | 'PENDING' | 'REJECTED';
  property: PropertyId;
  tenant: TenantId;
  period: {
    start: Date;
    end: Date;
  };
  pricing: {
    total: number;
    deposit: number;
    fees: Record<string, number>;
  };
  verificationResults?: {
    documents: boolean;
    tenant: boolean;
    property: boolean;
  };
}

@Injectable()
export class PropertyReservationProcess implements BusinessProcess<ReservationInput, ReservationOutput> {
  name = 'Property Reservation Process';
  description = 'Handles end-to-end property reservation flow with configurable business rules';

  constructor(
    private readonly propertyService: PropertyService,
    private readonly tenantService: TenantService,
    private readonly documentService: DocumentService
  ) {}

  steps = [
    {
      name: 'PropertyAvailabilityCheck',
      description: 'Verify property availability for the requested period',
      required: true,
      async execute(context: ProcessContext<ReservationInput>): Promise<ProcessResult<any>> {
        const { propertyId, startDate, endDate } = context.input;
        
        const isAvailable = await this.propertyService.checkAvailability(
          propertyId,
          { start: startDate, end: endDate }
        );

        if (!isAvailable) {
          return {
            success: false,
            error: new PropertyNotAvailableError(propertyId, { start: startDate, end: endDate }),
            context
          };
        }

        return {
          success: true,
          data: { isAvailable, propertyId },
          context
        };
      }
    },
    {
      name: 'TenantVerification',
      description: 'Verify tenant eligibility and background check',
      required: true,
      async execute(context: ProcessContext<ReservationInput>): Promise<ProcessResult<any>> {
        const { tenantId } = context.input;
        
        const verificationResult = await this.tenantService.verifyTenant(tenantId);

        if (!verificationResult.eligible) {
          return {
            success: false,
            error: new Error('Tenant verification failed: ' + verificationResult.reason),
            context
          };
        }

        return {
          success: true,
          data: { verificationResult },
          context
        };
      }
    },
    {
      name: 'DocumentProcessing',
      description: 'Process and verify required documents',
      required: true,
      async execute(context: ProcessContext<ReservationInput>): Promise<ProcessResult<any>> {
        const { documents = [] } = context.input;
        
        const documentResults = await Promise.all(
          documents.map(doc => this.documentService.verifyDocument(doc))
        );

        const allValid = documentResults.every(result => result.valid);
        if (!allValid) {
          return {
            success: false,
            error: new Error('Document verification failed'),
            context
          };
        }

        return {
          success: true,
          data: { documentResults },
          context
        };
      }
    },
    {
      name: 'PricingCalculation',
      description: 'Calculate total price including all fees',
      required: true,
      async execute(context: ProcessContext<ReservationInput>): Promise<ProcessResult<any>> {
        const { propertyId, startDate, endDate } = context.input;
        
        const pricing = await this.propertyService.calculatePricing(
          propertyId,
          { start: startDate, end: endDate }
        );

        return {
          success: true,
          data: { pricing },
          context
        };
      }
    }
  ];

  async validate(input: ReservationInput): Promise<ValidationResult> {
    const errors: string[] = [];

    if (!input.propertyId) errors.push('Property ID is required');
    if (!input.tenantId) errors.push('Tenant ID is required');
    if (!input.startDate || !input.endDate) errors.push('Start and end dates are required');
    if (input.startDate >= input.endDate) errors.push('End date must be after start date');

    // Additional validation from services
    const [propertyValid, tenantValid] = await Promise.all([
      this.propertyService.validateProperty(input.propertyId),
      this.tenantService.validateTenant(input.tenantId)
    ]);

    if (!propertyValid) errors.push('Invalid property ID');
    if (!tenantValid) errors.push('Invalid tenant ID');

    return {
      success: errors.length === 0,
      errors
    };
  }

  async execute(input: ReservationInput): Promise<ProcessResult<ReservationOutput>> {
    // Note: The actual execution will be handled by the ProcessEngine
    // This is just the default implementation
    const validationResult = await this.validate(input);
    if (!validationResult.success) {
      return {
        success: false,
        error: new Error(validationResult.errors?.join(', ')),
        context: {
          input,
          state: {},
          metadata: {
            processId: crypto.randomUUID(),
            startedAt: new Date(),
            completedSteps: []
          }
        }
      };
    }

    // Create reservation through property service
    const reservation = await this.propertyService.createReservation({
      propertyId: input.propertyId,
      tenantId: input.tenantId,
      period: {
        start: input.startDate,
        end: input.endDate
      }
    });

    return {
      success: true,
      data: {
        reservationId: reservation.id,
        status: reservation.status,
        property: reservation.propertyId,
        tenant: reservation.tenantId,
        period: {
          start: reservation.period.start,
          end: reservation.period.end
        },
        pricing: reservation.pricing,
        verificationResults: {
          documents: true,
          tenant: true,
          property: true
        }
      },
      context: {
        input,
        state: {},
        metadata: {
          processId: crypto.randomUUID(),
          startedAt: new Date(),
          completedSteps: []
        }
      }
    };
  }
}
