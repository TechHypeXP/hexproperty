import { ValueObject } from '../common/ValueObject';

export class Amenity extends ValueObject {
    private readonly _id: string;
    private readonly _name: string;
    private readonly _description: string;
    private readonly _category: string;
    private readonly _availability: boolean;

    constructor(
        id: string,
        name: string,
        description: string,
        category: string,
        availability: boolean = true
    ) {
        super();
        this._id = id;
        this._name = name;
        this._description = description;
        this._category = category;
        this._availability = availability;
    }

    // Getters
    get id(): string { return this._id; }
    get name(): string { return this._name; }
    get description(): string { return this._description; }
    get category(): string { return this._category; }
    get availability(): boolean { return this._availability; }

    // Value Object Implementation
    equals(other: Amenity): boolean {
        return this._id === other._id;
    }

    // Domain Validation
    isValid(): boolean {
        return (
            this._id?.length > 0 &&
            this._name?.length > 0 &&
            this._category?.length > 0
        );
    }

    // Factory Methods
    static createBasic(id: string, name: string, category: string): Amenity {
        return new Amenity(id, name, '', category);
    }
}
