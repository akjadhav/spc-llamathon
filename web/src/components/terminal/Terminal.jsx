import React, { useState, useEffect, use } from 'react'
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter'
import js from 'react-syntax-highlighter/dist/esm/languages/hljs/javascript'
import { atomOneDark } from 'react-syntax-highlighter/dist/esm/styles/hljs'

SyntaxHighlighter.registerLanguage('javascript', js)

const Terminal = ({ jobID }) => {
  const [fileContent, setFileContent] = useState(
    `
      //This is the content of the file \n
      function test() { \n
        console.log('Hello World');\n
      }\n
    `,
  )

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
      className='bg-gray-950 font-mono overflow-auto p-4 rounded-xl text-green-400 text-sm h-full'
    >
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
  )
}

export default Terminal
