import React, { useState, useEffect, use } from 'react'
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter'
import js from 'react-syntax-highlighter/dist/esm/languages/hljs/javascript'
import { atomOneDark } from 'react-syntax-highlighter/dist/esm/styles/hljs'
import TestDisplay from './TestDisplay'
import ClipLoader from 'react-spinners/ClipLoader'

SyntaxHighlighter.registerLanguage('javascript', js)

const Terminal = ({ fileSelectedPath }) => {
  const [file, setFile] = useState(undefined)
  const [loading, setLoading] = useState(false)
  const [highlightedLineNumbers, setHighlightedLineNumbers] = useState(new Set())

  useEffect(() => {
    const fetchData = async () => {
      if (fileSelectedPath === undefined) return

      setLoading(true)
      console.log("fetching file: ", fileSelectedPath)
      try {
        const response = await fetch('/api/get-file', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ fileName: fileSelectedPath }),
        })

        if (!response.ok) {
          throw new Error('Failed to fetch file')
        }

        const data = await response.json()
        console.log(data)
        // Handle the file content here
        setLoading(false)
        setFile(data)
      } catch (error) {
        setLoading(false)
        console.error('Error:', error)
        // Handle the error here

        setFile({
          type: 'test',
          data: `
// Import the target function
const add = require('./example').add;

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

    // Test case: Adding two zeros
    it('should add two zeros correctly', () => {
        expect(add(0, 0)).toBe(0);
    });

    // Test case: Adding a number and zero
    it('should add a number and zero correctly', () => {
        expect(add(5, 0)).toBe(5);
    });

    // Test case: Adding non-integer numbers
    it('should add non-integer numbers correctly', () => {
        expect(add(2.5, 3.7)).toBe(6.2);
    });

    // Test case: Adding non-numeric values
    it('should return NaN when adding non-numeric values', () => {
        expect(add('a', 2)).toBeNaN();
    });

    // Test case: Adding undefined values
    it('should return NaN when adding undefined values', () => {
        expect(add(undefined, 2)).toBeNaN();
    });

    // Test case: Adding null values
    it('should return NaN when adding null values', () => {
        expect(add(null, 2)).toBeNaN();
    });
});// Import the target function
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
              `,
          failedLines: [1, 2, 3, 6, 7, 8, 61, 62, 63, 64],
          testStatus: { suite1: { func1: false, func2: true } },
        })
      }
    }

    fetchData()
  }, [fileSelectedPath])

  useEffect(() => {
    setHighlightedLineNumbers(file && new Set(file.failedLines))
  }, [file])

  return (
    <div className='relative custom-height'
      style={{ 'overflow-y': 'auto', height: '700px' }}>
      {loading && (
        <div className='absolute inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75 z-10'>
          <ClipLoader color="white" />
        </div>
      )}
      <div
        id='mock-terminal'
        className='bg-gray-950 pt-4 font-mono overflow-auto rounded-xl text-green-400 text-sm h-full flex'
      >
        <div>
          {file &&
            file.data
              .split('\n')
              .map((_, index) => (
                <div
                  key={index}
                  className={`w-2 ${highlightedLineNumbers !== undefined &&
                    highlightedLineNumbers.has(index) &&
                    'bg-red-500'
                    }`}
                  style={{ height: '1.43em' }}
                />
              ))}
        </div>
        <div className="pl-2 text-gray-500 text-xs">
          {file &&
            file.data
              .split('\n')
              .map((_, index) => (
                <div
                  key={index}
                  style={{
                    height: '1.665em',
                    display: 'flex',
                    alignItems: 'flex-end'
                  }}
                >
                  {index + 1}
                </div>
              ))}
        </div>
        <div className='pl-2 flex-grow'>
          <SyntaxHighlighter
            language='javascript'
            style={atomOneDark}
            customStyle={{
              backgroundColor: 'transparent',
              padding: 0,
              margin: 0,
            }}
          >
            {file && file.data}
          </SyntaxHighlighter>
        </div>
      </div>
      {file && Object.keys(file.testStatus).length > 0 &&
        <TestDisplay testStatus={file.testStatus} />
      }

      {/* Test Display Demo */}
      {/* {
        <TestDisplay testStatus={{ suite1: { func1: false, func2: true }, suite2: { func1: true, func2: true } }} />
      } */}
    </div>
  )
}

export default Terminal
