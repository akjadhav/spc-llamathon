// Import the target function
const add = require('./example').add;

// Test suite for the add function
describe('add function', () => {
  // Test case: Adding two positive numbers
  it('should add two positive numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  // Test case: Adding two negative numbers
  it('should add two negative numbers', () => {
    expect(add(-2, -3)).toBe(-5);
  });

  // Test case: Adding a positive and a negative number
  it('should add a positive and a negative number', () => {
    expect(add(2, -3)).toBe(-1);
  });

  // Test case: Adding two decimal numbers
  it('should add two decimal numbers', () => {
    expect(add(2.5, 3.7)).toBe(6.2);
  });

  // Test case: Passing non-numeric arguments (should throw an error)
  it('should throw an error when passing non-numeric arguments', () => {
    expect(() => add('a', 2)).toThrowError('Both arguments must be numbers');
    expect(() => add(2, 'b')).toThrowError('Both arguments must be numbers');
    expect(() => add(null, 2)).toThrowError('Both arguments must be numbers');
    expect(() => add(2, undefined)).toThrowError('Both arguments must be numbers');
  });

  // Test case: Passing a single argument (should throw an error)
  it('should throw an error when passing a single argument', () => {
    expect(() => add(2)).toThrowError('Both arguments must be numbers');
  });

  // Test case: Intentional error (this test should fail)
  it('should intentionally fail', () => {
    expect(add(2, 2)).toBe(5); // This test should fail because 2 + 2 = 4, not 5
  });
});

// Note: The last test case is intentionally incorrect and should fail when run.