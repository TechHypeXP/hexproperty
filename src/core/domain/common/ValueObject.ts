export abstract class ValueObject {
    abstract equals(other: ValueObject): boolean;
    abstract isValid(): boolean;
}
