// Import the target function
const multiply = require('./example').multiply;

// Test suite for the multiply function
describe('multiply function', () => {
  // Test case for multiplying two positive numbers
  it('should multiply two positive numbers correctly', () => {
    expect(multiply(2, 3)).toBe(6);
    expect(multiply(4, 5)).toBe(20);
  });

  // Test case for multiplying two negative numbers
  it('should multiply two negative numbers correctly', () => {
    expect(multiply(-2, -3)).toBe(6);
    expect(multiply(-4, -5)).toBe(20);
  });

  // Test case for multiplying a positive and a negative number
  it('should multiply a positive and a negative number correctly', () => {
    expect(multiply(2, -3)).toBe(-6);
    expect(multiply(-4, 5)).toBe(-20);
  });

  // Test case for multiplying zero with a number
  it('should multiply zero with a number correctly', () => {
    expect(multiply(0, 2)).toBe(0);
    expect(multiply(3, 0)).toBe(0);
  });

  // Test case for multiplying two zeros
  it('should multiply two zeros correctly', () => {
    expect(multiply(0, 0)).toBe(0);
  });

  // Test case for multiplying decimal numbers
  it('should multiply decimal numbers correctly', () => {
    expect(multiply(2.5, 3.5)).toBeCloseTo(8.75);
    expect(multiply(-2.5, 3.5)).toBeCloseTo(-8.75);
  });

  // Test case for multiplying large numbers
  it('should multiply large numbers correctly', () => {
    expect(multiply(1000, 2000)).toBe(2000000);
    expect(multiply(-1000, 2000)).toBe(-2000000);
  });
});