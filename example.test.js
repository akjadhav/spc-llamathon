// Import the target function and related functions
const {
  add,
  multiply,
  square,
  sumOfSquares,
  factorial,
  isEven,
  isOdd,
  fibonacci,
} = require('./example');

// Test suite for the target function: add
describe('add function', () => {
  // Test case 1: Adding two positive numbers
  it('should return the sum of two positive numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  // Test case 2: Adding two negative numbers
  it('should return the sum of two negative numbers', () => {
    expect(add(-2, -3)).toBe(-5);
  });

  // Test case 3: Adding a positive and a negative number
  it('should return the sum of a positive and a negative number', () => {
    expect(add(2, -3)).toBe(-1);
  });

  // Test case 4: Adding zero to a number
  it('should return the number when adding zero', () => {
    expect(add(2, 0)).toBe(2);
  });

  // Test case 5: Adding two decimal numbers
  it('should return the sum of two decimal numbers', () => {
    expect(add(2.5, 3.7)).toBeCloseTo(6.2);
  });
});

// Additional test cases to ensure the target function works correctly with other functions
describe('integration with other functions', () => {
  // Test case 1: Using the add function with the multiply function
  it('should return the correct result when used with multiply', () => {
    expect(add(multiply(2, 3), 4)).toBe(10);
  });

  // Test case 2: Using the add function with the square function
  it('should return the correct result when used with square', () => {
    expect(add(square(2), 3)).toBe(7);
  });

  // Test case 3: Using the add function with the sumOfSquares function
  it('should return the correct result when used with sumOfSquares', () => {
    expect(sumOfSquares(2, 3)).toBe(add(square(2), square(3)));
  });

  // Test case 4: Using the add function with the factorial function
  it('should return the correct result when used with factorial', () => {
    expect(add(factorial(3), 2)).toBe(8);
  });

  // Test case 5: Using the add function with the isEven and isOdd functions
  it('should return the correct result when used with isEven and isOdd', () => {
    expect(isEven(add(2, 2))).toBe(true);
    expect(isOdd(add(2, 3))).toBe(true);
  });

  // Test case 6: Using the add function with the fibonacci function
  it('should return the correct result when used with fibonacci', () => {
    expect(add(fibonacci(3), fibonacci(4))).toBe(5);
  });
});