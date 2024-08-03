// utils.js

// Function to add two numbers
function add(a, b) {
    return a + b;
}

// Function to multiply two numbers
function multiply(a, b) {
    return a * b;
}

// Function to square a number using the multiply function
function square(x) {
    return multiply(x, x);
}

// Function to calculate the sum of squares of two numbers
function sumOfSquares(a, b) {
    return add(square(a), square(b));
}

// Function to calculate the factorial of a number
function factorial(n) {
    if (n === 0) {
        return 1;
    }
    return multiply(n, factorial(n - 1));
}

// Function to check if a number is even
function isEven(n) {
    return n % 2 === 0;
}

// Function to check if a number is odd using the isEven function
function isOdd(n) {
    return !isEven(n);
}

// Function to calculate the nth Fibonacci number
function fibonacci(n) {
    if (n <= 1) {
        return n;
    }
    return add(fibonacci(n - 1), fibonacci(n - 2));
}

// Exporting functions for use in other modules
module.exports = add
