// Import the target function
const add = require('./example').add;

// Test suite for the add function
describe('add function', () => {
  // Test case for adding two positive numbers
  it('should add two positive numbers', () => {
    // Arrange
    const a = 2;
    const b = 3;
    const expected = 5;

    // Act
    const result = add(a, b);

    // Assert
    expect(result).toBe(expected);
  });

  // Test case for adding two negative numbers
  it('should add two negative numbers', () => {
    // Arrange
    const a = -2;
    const b = -3;
    const expected = -5;

    // Act
    const result = add(a, b);

    // Assert
    expect(result).toBe(expected);
  });

  // Test case for adding a positive and a negative number
  it('should add a positive and a negative number', () => {
    // Arrange
    const a = 2;
    const b = -3;
    const expected = -1;

    // Act
    const result = add(a, b);

    // Assert
    expect(result).toBe(expected);
  });

  // Test case for adding two decimal numbers
  it('should add two decimal numbers', () => {
    // Arrange
    const a = 2.5;
    const b = 3.7;
    const expected = 6.2;

    // Act
    const result = add(a, b);

    // Assert
    expect(result).toBeCloseTo(expected);
  });

  // Test case for adding zero to a number
  it('should add zero to a number', () => {
    // Arrange
    const a = 5;
    const b = 0;
    const expected = 5;

    // Act
    const result = add(a, b);

    // Assert
    expect(result).toBe(expected);
  });

  // Test case for adding two zeros
  it('should add two zeros', () => {
    // Arrange
    const a = 0;
    const b = 0;
    const expected = 0;

    // Act
    const result = add(a, b);

    // Assert
    expect(result).toBe(expected);
  });
});