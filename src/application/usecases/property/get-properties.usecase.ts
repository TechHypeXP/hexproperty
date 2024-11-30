import { Property, TenantId } from '@/domain/models/property/property';
import { PropertyService } from '@/domain/services/property.service';

export class GetPropertiesUseCase {
  constructor(private readonly propertyService: PropertyService) {}

  async execute(tenantId: TenantId): Promise<Property[]> {
    try {
      return await this.propertyService.getPropertiesByTenant(tenantId);
    } catch (error) {
      // Add proper error handling and logging here
      throw error;
    }
  }
}
