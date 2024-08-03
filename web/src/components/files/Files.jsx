import React, { useState, useEffect, use } from 'react';
import File from './File';
import FilesRow from './FilesRow';

const Files = ({ jobID }) => {
    const [files, setFiles] = useState([
        new File("./", "index.js"),
        new File("./", "page.js"),
    ]);

    const [fileSelectedIndex, setFileSelectedIndex] = useState(0);

    useEffect(() => {
        const fetchData = async () => {
            //   try {
            //     const response = await fetch(api_endpoint + '/' + jobID + '/logs');
            //     var jsonData = await response.json();

            //     var logs = jsonData.response;
            //     var setJsonData = logs.split('\n');

            //     setOutputs(setJsonData);
            //   } catch (error) {
            //     console.error('Failed to fetch data:', error);
            //   }
        };

        if (jobID !== '') fetchData();
        const intervalId = setInterval(fetchData, 1000);

        return () => clearInterval(intervalId);
    }, [jobID]);

    // Effect to make sure the terminal is scrolled to the bottom on new output
    useEffect(() => {
        const terminal = document.getElementById('mock-terminal');
        if (terminal) {
            terminal.scrollTop = terminal.scrollHeight;
        }
    }, [files]);

    return (
        <div
            id='mock-terminal'
            className='bg-gray-950 custom-height font-mono overflow-auto text-green-400 text-sm w-full'
            style={{ height: '700px' }}>
            {files.map((file, index) => (
                <FilesRow key={index} file={file} index={index} fileSelectedIndex={fileSelectedIndex} setFileSelectedIndex={setFileSelectedIndex}></FilesRow>
            ))}
        </div>
    );
};

export default Files;
