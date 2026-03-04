import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Utility function to merge Tailwind CSS classes using clsx and tailwind-merge.
 * This ensures that conflicting Tailwind classes are handled correctly.
 *
 * @param {ClassValue[]} inputs - An array of class names, objects, or arrays to merge.
 * @returns {string} The merged class name string.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
