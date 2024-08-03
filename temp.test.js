// Import the target function and related context functions
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
  // Test case: Adding two positive numbers
  it('should add two positive numbers correctly', () => {
    expect(add(2, 3)).toBe(5);
  });

  // Test case: Adding two negative numbers
  it('should add two negative numbers correctly', () => {
    expect(add(-2, -3)).toBe(-5);
  });

  // Test case: Adding a positive and a negative number
  it('should add a positive and a negative number correctly', () => {
    expect(add(2, -3)).toBe(-1);
  });

  // Test case: Adding two zero numbers
  it('should add two zero numbers correctly', () => {
    expect(add(0, 0)).toBe(0);
  });

  // Test case: Adding a number with a non-numeric value
  it('should throw an error when adding a number with a non-numeric value', () => {
    expect(() => add(2, 'a')).toThrowError(TypeError);
  });

  // Test case: Adding two non-numeric values
  it('should throw an error when adding two non-numeric values', () => {
    expect(() => add('a', 'b')).toThrowError(TypeError);
  });

  // Test case: Checking the return type of the add function
  it('should return a number when adding two numbers', () => {
    expect(typeof add(2, 3)).toBe('number');
  });
});

// Additional tests to ensure the target function works correctly with other functions
describe('integration tests', () => {
  // Test case: Using the add function with the multiply function
  it('should work correctly with the multiply function', () => {
    expect(add(multiply(2, 2), multiply(3, 3))).toBe(13);
  });

  // Test case: Using the add function with the square function
  it('should work correctly with the square function', () => {
    expect(add(square(2), square(3))).toBe(13);
  });

  // Test case: Using the add function with the sumOfSquares function
  it('should work correctly with the sumOfSquares function', () => {
    expect(sumOfSquares(2, 3)).toBe(13);
  });

  // Test case: Using the add function with the factorial function
  it('should work correctly with the factorial function', () => {
    expect(add(factorial(2), factorial(3))).toBe(8);
  });

  // Test case: Using the add function with the isEven and isOdd functions
  it('should work correctly with the isEven and isOdd functions', () => {
    expect(isEven(add(2, 2))).toBe(true);
    expect(isOdd(add(2, 3))).toBe(true);
  });

  // Test case: Using the add function with the fibonacci function
  it('should work correctly with the fibonacci function', () => {
    expect(add(fibonacci(2), fibonacci(3))).toBe(3);
  });
});