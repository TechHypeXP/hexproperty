import { Entity } from '../common/Entity';
import { PropertyType } from '../enums/PropertyType';
import { Address } from '../valueObjects/Address';
import { Amenity } from '../valueObjects/Amenity';
import { PropertyStatus } from '../enums/PropertyStatus';

export class Property extends Entity {
    private _name: string;
    private _type: PropertyType;
    private _address: Address;
    private _units: number;
    private _amenities: Amenity[];
    private _status: PropertyStatus;
    private _securityGateEnabled: boolean;
    private _documentVerificationRequired: boolean;

    constructor(
        id: string,
        name: string,
        type: PropertyType,
        address: Address,
        units: number,
        amenities: Amenity[] = [],
        status: PropertyStatus = PropertyStatus.ACTIVE,
        securityGateEnabled: boolean = false,
        documentVerificationRequired: boolean = false
    ) {
        super(id);
        this._name = name;
        this._type = type;
        this._address = address;
        this._units = units;
        this._amenities = amenities;
        this._status = status;
        this._securityGateEnabled = securityGateEnabled;
        this._documentVerificationRequired = documentVerificationRequired;
    }

    // Getters
    get name(): string { return this._name; }
    get type(): PropertyType { return this._type; }
    get address(): Address { return this._address; }
    get units(): number { return this._units; }
    get amenities(): Amenity[] { return [...this._amenities]; }
    get status(): PropertyStatus { return this._status; }
    get securityGateEnabled(): boolean { return this._securityGateEnabled; }
    get documentVerificationRequired(): boolean { return this._documentVerificationRequired; }

    // Business Logic Methods
    enableSecurityGate(): void {
        this._securityGateEnabled = true;
    }

    disableSecurityGate(): void {
        this._securityGateEnabled = false;
    }

    requireDocumentVerification(): void {
        this._documentVerificationRequired = true;
    }

    addAmenity(amenity: Amenity): void {
        if (!this._amenities.some(a => a.equals(amenity))) {
            this._amenities.push(amenity);
        }
    }

    removeAmenity(amenityId: string): void {
        this._amenities = this._amenities.filter(a => a.id !== amenityId);
    }

    deactivate(): void {
        this._status = PropertyStatus.INACTIVE;
    }

    activate(): void {
        this._status = PropertyStatus.ACTIVE;
    }

    // Domain Validation
    validate(): boolean {
        return (
            this._name?.length > 0 &&
            this._type != null &&
            this._address?.isValid() &&
            this._units > 0
        );
    }
}
