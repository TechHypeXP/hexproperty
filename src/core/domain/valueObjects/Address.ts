import { ValueObject } from '../common/ValueObject';

export class Address extends ValueObject {
    private readonly _street: string;
    private readonly _city: string;
    private readonly _state: string;
    private readonly _postalCode: string;
    private readonly _country: string;
    private readonly _coordinates?: { latitude: number; longitude: number };

    constructor(
        street: string,
        city: string,
        state: string,
        postalCode: string,
        country: string,
        coordinates?: { latitude: number; longitude: number }
    ) {
        super();
        this._street = street;
        this._city = city;
        this._state = state;
        this._postalCode = postalCode;
        this._country = country;
        this._coordinates = coordinates;
    }

    // Getters
    get street(): string { return this._street; }
    get city(): string { return this._city; }
    get state(): string { return this._state; }
    get postalCode(): string { return this._postalCode; }
    get country(): string { return this._country; }
    get coordinates(): { latitude: number; longitude: number } | undefined { 
        return this._coordinates ? { ...this._coordinates } : undefined;
    }

    // Value Object Implementation
    equals(other: Address): boolean {
        return (
            this._street === other._street &&
            this._city === other._city &&
            this._state === other._state &&
            this._postalCode === other._postalCode &&
            this._country === other._country
        );
    }

    // Domain Validation
    isValid(): boolean {
        return (
            this._street?.length > 0 &&
            this._city?.length > 0 &&
            this._state?.length > 0 &&
            this._postalCode?.length > 0 &&
            this._country?.length > 0
        );
    }

    // Formatting
    toString(): string {
        return `${this._street}, ${this._city}, ${this._state} ${this._postalCode}, ${this._country}`;
    }

    // Factory Methods
    static fromString(addressString: string): Address | null {
        try {
            const parts = addressString.split(',').map(part => part.trim());
            if (parts.length >= 5) {
                const [street, city, state, postalCode, country] = parts;
                return new Address(street, city, state, postalCode, country);
            }
            return null;
        } catch {
            return null;
        }
    }
}
