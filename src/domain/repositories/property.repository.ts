import { Property, PropertyId, CreatePropertyDTO, UpdatePropertyDTO, TenantId } from '../models/property/property';

export interface PropertyRepository {
  findById(id: PropertyId): Promise<Property | null>;
  findByTenantId(tenantId: TenantId): Promise<Property[]>;
  create(data: CreatePropertyDTO): Promise<Property>;
  update(data: UpdatePropertyDTO): Promise<Property>;
  delete(id: PropertyId): Promise<void>;
  
  // Additional repository methods
  findAvailableProperties(tenantId: TenantId): Promise<Property[]>;
  findByStatus(tenantId: TenantId, status: PropertyStatus): Promise<Property[]>;
  updateStatus(id: PropertyId, status: PropertyStatus): Promise<Property>;
}
