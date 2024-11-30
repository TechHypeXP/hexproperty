import { Brand } from '../../utils/brand';

// Branded types for type-safety
export type PropertyId = Brand<string, 'PropertyId'>;
export type LocationId = Brand<string, 'LocationId'>;

// Value Objects
export interface GeoLocation {
  latitude: number;
  longitude: number;
  accuracy?: number;
}

export interface Address {
  street: string;
  city: string;
  state: string;
  country: string;
  postalCode: string;
  formatted?: string;
}

export interface Location {
  id: LocationId;
  address: Address;
  coordinates: GeoLocation;
}

// Enums
export enum PropertyStatus {
  Available = 'available',
  Reserved = 'reserved',
  Maintenance = 'maintenance',
  Offline = 'offline'
}

export enum PropertyType {
  Apartment = 'apartment',
  House = 'house',
  Condo = 'condo',
  Villa = 'villa',
  Commercial = 'commercial'
}

export enum AmenityType {
  Pool = 'pool',
  Gym = 'gym',
  Parking = 'parking',
  Security = 'security',
  Elevator = 'elevator',
  AirConditioning = 'air_conditioning',
  Heating = 'heating',
  Internet = 'internet'
}

// Main Property Interface
export interface Property {
  id: PropertyId;
  name: string;
  description: string;
  type: PropertyType;
  status: PropertyStatus;
  location: Location;
  amenities: AmenityType[];
  specifications: {
    bedrooms: number;
    bathrooms: number;
    totalArea: number;
    parkingSpots?: number;
    yearBuilt?: number;
  };
  pricing: {
    basePrice: number;
    currency: string;
    minimumStay?: number;
    maximumStay?: number;
  };
  media: {
    images: string[];
    videos?: string[];
    virtualTour?: string;
  };
  metadata: {
    createdAt: Date;
    updatedAt: Date;
    lastMaintenanceDate?: Date;
    nextMaintenanceDate?: Date;
  };
}

// DTOs
export interface CreatePropertyDTO extends Omit<Property, 'id' | 'metadata'> {
  metadata?: Partial<Property['metadata']>;
}

export interface UpdatePropertyDTO extends Partial<Omit<Property, 'id' | 'metadata'>> {
  metadata?: Partial<Property['metadata']>;
}

// Validation Schemas (to be used with Zod)
export interface PropertyValidationRules {
  name: {
    minLength: number;
    maxLength: number;
  };
  description: {
    minLength: number;
    maxLength: number;
  };
  pricing: {
    minBasePrice: number;
    maxBasePrice: number;
  };
}
