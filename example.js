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

// Function to calculate the greatest common divisor of two numbers
function gcd(a, b) {
    if (b === 0) {
        return a;
    }
    return gcd(b, a % b);
}

// Function to calculate the least common multiple of two numbers using the gcd function
function lcm(a, b) {
    return multiply(a, b) / gcd(a, b);
}

// Function to calculate the average of an array of numbers
function average(arr) {
    const sum = arr.reduce(add, 0);
    return sum / arr.length;
}

// Function to find the maximum number in an array using the Math.max function
function max(arr) {
    return Math.max(...arr);
}

// Function to find the minimum number in an array using the Math.min function
function min(arr) {
    return Math.min(...arr);
}

// Function to calculate the range of an array of numbers using the max and min functions
function range(arr) {
    return subtract(max(arr), min(arr));
}

// Function to subtract two numbers
function subtract(a, b) {
    return a - b;
}

// Function to calculate the median of an array of numbers
function median(arr) {
    const sorted = arr.slice().sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    if (isEven(sorted.length)) {
        return average([sorted[mid - 1], sorted[mid]]);
    }
    return sorted[mid];
}

// Function to calculate the mode of an array of numbers
function mode(arr) {
    const frequency = {};
    arr.forEach(num => {
        if (!frequency[num]) {
            frequency[num] = 0;
        }
        frequency[num]++;
    });
    let maxFreq = 0;
    let mode = [];
    for (const num in frequency) {
        if (frequency[num] > maxFreq) {
            maxFreq = frequency[num];
            mode = [Number(num)];
        } else if (frequency[num] === maxFreq) {
            mode.push(Number(num));
        }
    }
    if (mode.length === arr.length) {
        return [];
    }
    return mode;
}

// Exporting functions for use in other modules
module.exports = {
    add,
    multiply,
    square,
    sumOfSquares,
    factorial,
    isEven,
    isOdd,
    fibonacci,
    gcd,
    lcm,
    average,
    max,
    min,
    range,
    subtract,
    median,
    mode
};
