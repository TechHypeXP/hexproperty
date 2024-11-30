export abstract class Entity {
    private readonly _id: string;

    protected constructor(id: string) {
        this._id = id;
    }

    get id(): string {
        return this._id;
    }

    equals(other: Entity): boolean {
        if (other == null) {
            return false;
        }
        return this._id === other._id;
    }

    abstract validate(): boolean;
}
