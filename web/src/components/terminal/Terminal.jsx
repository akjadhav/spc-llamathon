import React, { useState, useEffect, use } from 'react'
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter'
import js from 'react-syntax-highlighter/dist/esm/languages/hljs/javascript'
import { atomOneDark } from 'react-syntax-highlighter/dist/esm/styles/hljs'

SyntaxHighlighter.registerLanguage('javascript', js)

const Terminal = ({ jobID }) => {
  const [fileContent, setFileContent] = useState(
    `
      //This is the content of the file
      function test() {
        console.log('Hello World');
      }\n
    `,
  )

  const [highlightedLineNumbers, setHighlightedLineNumbers] = useState(new Set([1, 2, 3, 6, 7, 8, 10, 11, 12, 13, 14]))

  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       const response = await fetch(api_endpoint + '/' + jobID + '/logs');
  //       var jsonData = await response.json();

  //       var logs = jsonData.response;

  //       var setJsonData = logs.split('\n');

  //       // setOutputs(setJsonData);
  //     } catch (error) {
  //       console.error('Failed to fetch data:', error);
  //     }
  //   };

  //   if (jobID !== '') fetchData();
  //   const intervalId = setInterval(fetchData, 1000);

  //   return () => clearInterval(intervalId);
  // }, [jobID]);

  return (
    <div
      id='mock-terminal'
      className='bg-gray-950 font-mono overflow-auto rounded-xl text-green-400 text-sm h-full flex'
    >
      <div className='line-numbers relative flex-shrink-0 pt-4'>
        {fileContent.split('\n').map((_, index) => (
          <div
            key={index}
            className={`h-6 w-2 ${(highlightedLineNumbers.has(index)) && 'bg-red-500'}`}
          />
        ))}
      </div>
      <div className='pl-2 pt-4 flex-grow'>
        <SyntaxHighlighter
          language='javascript'
          style={atomOneDark}
          customStyle={{
            backgroundColor: 'transparent',
            padding: 0,
            margin: 0,
          }}
        >
          {fileContent}
        </SyntaxHighlighter>
      </div>
    </div>
  )
}

export default Terminal
