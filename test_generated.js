// jest test suite for add function

describe('add function', () => {
  // test case for adding two positive numbers
  it('should add two positive numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  // test case for adding two negative numbers
  it('should add two negative numbers', () => {
    expect(add(-2, -3)).toBe(-5);
  });

  // test case for adding a positive and a negative number
  it('should add a positive and a negative number', () => {
    expect(add(2, -3)).toBe(-1);
  });

  // test case for adding two zeros
  it('should add two zeros', () => {
    expect(add(0, 0)).toBe(0);
  });

  // test case for adding a number and zero
  it('should add a number and zero', () => {
    expect(add(5, 0)).toBe(5);
  });

  // test case for non-numeric input
  it('should throw an error for non-numeric input', () => {
    expect(() => add('a', 2)).toThrowError('Both arguments must be numbers');
  });

  // test case for non-numeric input (second argument)
  it('should throw an error for non-numeric input (second argument)', () => {
    expect(() => add(2, 'b')).toThrowError('Both arguments must be numbers');
  });

  // test case for non-numeric input (both arguments)
  it('should throw an error for non-numeric input (both arguments)', () => {
    expect(() => add('a', 'b')).toThrowError('Both arguments must be numbers');
  });

  // test case for null input
  it('should throw an error for null input', () => {
    expect(() => add(null, 2)).toThrowError('Both arguments must be numbers');
  });

  // test case for undefined input
  it('should throw an error for undefined input', () => {
    expect(() => add(undefined, 2)).toThrowError('Both arguments must be numbers');
  });
});