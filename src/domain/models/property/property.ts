import { Brand } from '@/types/utils/brand';

// Branded types for type-safe IDs
export type PropertyId = Brand<string, 'PropertyId'>;
export type TenantId = Brand<string, 'TenantId'>;

export enum PropertyStatus {
  AVAILABLE = 'AVAILABLE',
  RENTED = 'RENTED',
  MAINTENANCE = 'MAINTENANCE',
  RESERVED = 'RESERVED'
}

export enum PropertyType {
  APARTMENT = 'APARTMENT',
  HOUSE = 'HOUSE',
  CONDO = 'CONDO',
  COMMERCIAL = 'COMMERCIAL'
}

export interface PropertyAddress {
  street: string;
  city: string;
  state: string;
  zipCode: string;
  country: string;
}

export interface Property {
  id: PropertyId;
  tenantId: TenantId;
  name: string;
  description: string;
  type: PropertyType;
  status: PropertyStatus;
  address: PropertyAddress;
  monthlyRent: number;
  bedrooms: number;
  bathrooms: number;
  squareFootage: number;
  amenities: string[];
  createdAt: Date;
  updatedAt: Date;
}

export interface CreatePropertyDTO {
  tenantId: TenantId;
  name: string;
  description: string;
  type: PropertyType;
  address: PropertyAddress;
  monthlyRent: number;
  bedrooms: number;
  bathrooms: number;
  squareFootage: number;
  amenities: string[];
}

export interface UpdatePropertyDTO extends Partial<CreatePropertyDTO> {
  id: PropertyId;
}
