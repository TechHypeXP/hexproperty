import { Injectable } from '@/support/di/decorators';
import { Property, PropertyId, TenantId, CreatePropertyDTO, UpdatePropertyDTO, PropertyStatus } from '../models/property/property';
import { PropertyRepository } from '../repositories/property.repository';

export interface DateRange {
  start: Date;
  end: Date;
}

export interface ReservationDetails {
  propertyId: PropertyId;
  tenantId: TenantId;
  period: DateRange;
}

export interface PricingDetails {
  total: number;
  deposit: number;
  fees: Record<string, number>;
}

@Injectable()
export class PropertyService {
  constructor(private readonly propertyRepository: PropertyRepository) {}

  async getProperty(id: PropertyId): Promise<Property | null> {
    return this.propertyRepository.findById(id);
  }

  async getPropertiesByTenant(tenantId: TenantId): Promise<Property[]> {
    return this.propertyRepository.findByTenantId(tenantId);
  }

  async createProperty(data: CreatePropertyDTO): Promise<Property> {
    // Add business logic validation here
    this.validatePropertyData(data);
    return this.propertyRepository.create(data);
  }

  async updateProperty(data: UpdatePropertyDTO): Promise<Property> {
    const existing = await this.propertyRepository.findById(data.id);
    if (!existing) {
      throw new Error(`Property with ID ${data.id} not found`);
    }

    this.validatePropertyData(data);
    return this.propertyRepository.update(data);
  }

  async deleteProperty(id: PropertyId): Promise<void> {
    const existing = await this.propertyRepository.findById(id);
    if (!existing) {
      throw new Error(`Property with ID ${id} not found`);
    }

    return this.propertyRepository.delete(id);
  }

  async getAvailableProperties(tenantId: TenantId): Promise<Property[]> {
    return this.propertyRepository.findAvailableProperties(tenantId);
  }

  async updatePropertyStatus(id: PropertyId, status: PropertyStatus): Promise<Property> {
    const existing = await this.propertyRepository.findById(id);
    if (!existing) {
      throw new Error(`Property with ID ${id} not found`);
    }

    return this.propertyRepository.updateStatus(id, status);
  }

  async checkAvailability(propertyId: PropertyId, dateRange: DateRange): Promise<boolean> {
    // Implementation would check against reservations and property status
    return true;
  }

  async validateProperty(propertyId: PropertyId): Promise<boolean> {
    const property = await this.propertyRepository.findById(propertyId);
    return !!property;
  }

  async calculatePricing(propertyId: PropertyId, dateRange: DateRange): Promise<PricingDetails> {
    const property = await this.propertyRepository.findById(propertyId);
    if (!property) {
      throw new Error('Property not found');
    }

    // Calculate number of days
    const days = Math.ceil(
      (dateRange.end.getTime() - dateRange.start.getTime()) / (1000 * 60 * 60 * 24)
    );

    // Basic pricing calculation
    const total = property.monthlyRent * (days / 30);
    const deposit = property.monthlyRent * 0.5;

    return {
      total,
      deposit,
      fees: {
        service: total * 0.1,
        cleaning: 150
      }
    };
  }

  async createReservation(details: ReservationDetails): Promise<{
    id: string;
    propertyId: PropertyId;
    tenantId: TenantId;
    status: 'CONFIRMED' | 'PENDING' | 'REJECTED';
    period: DateRange;
    pricing: PricingDetails;
  }> {
    // Validate property exists
    const property = await this.propertyRepository.findById(details.propertyId);
    if (!property) {
      throw new Error('Property not found');
    }

    // Check availability
    const isAvailable = await this.checkAvailability(details.propertyId, details.period);
    if (!isAvailable) {
      throw new Error('Property not available for the requested period');
    }

    // Calculate pricing
    const pricing = await this.calculatePricing(details.propertyId, details.period);

    // Create reservation (in a real implementation, this would be handled by a ReservationRepository)
    return {
      id: crypto.randomUUID(),
      propertyId: details.propertyId,
      tenantId: details.tenantId,
      status: 'CONFIRMED',
      period: details.period,
      pricing
    };
  }

  private validatePropertyData(data: Partial<CreatePropertyDTO>): void {
    if (data.monthlyRent !== undefined && data.monthlyRent <= 0) {
      throw new Error('Monthly rent must be greater than 0');
    }

    if (data.bedrooms !== undefined && data.bedrooms < 0) {
      throw new Error('Number of bedrooms cannot be negative');
    }

    if (data.bathrooms !== undefined && data.bathrooms < 0) {
      throw new Error('Number of bathrooms cannot be negative');
    }

    if (data.squareFootage !== undefined && data.squareFootage <= 0) {
      throw new Error('Square footage must be greater than 0');
    }
  }
}
