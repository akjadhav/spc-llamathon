import React, { useState, useEffect, use } from 'react';
import File from './File';
import FilesRow from './FilesRow';

const Files = ({ jobID, fileSelectedPath, setFileSelectedPath, files, setFiles }) => {
    // const [files, setFiles] = useState([
    //     new File("./", "index.js"),
    //     new File("./", "page.js"),
    // ]);


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

    return (
        <div className='h-full flex flex-col'>
            <div
                id='mock-terminal'
                className='bg-gray-950 font-mono overflow-auto text-green-400 text-sm space-y-2 h-full'>
                {files.map((file, index) => (
                    <FilesRow key={index} file={file} fileSelectedPath={fileSelectedPath} setFileSelectedPath={setFileSelectedPath} />
                ))}
            </div>
        </div >
    );
};

export default Files;
