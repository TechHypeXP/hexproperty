/**
 * Utility type for creating branded types
 * This helps prevent mixing up different types of IDs or other primitives
 */
export type Brand<K, T> = K & { __brand: T };

/**
 * Helper function to create a branded type
 */
export function brand<K, T>(k: K): Brand<K, T> {
  return k as Brand<K, T>;
}

/**
 * Helper function to validate and create a branded type
 */
export function createBrand<K, T>(k: K, validator: (k: K) => boolean): Brand<K, T> | null {
  if (validator(k)) {
    return brand<K, T>(k);
  }
  return null;
}
