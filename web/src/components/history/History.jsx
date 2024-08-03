import React, { useState, useEffect, use } from 'react';
import { api_endpoint } from '../../api_endpoint';
import HistoryRow from './HistoryRow';
import HistoryItem from './HistoryItem';

const History = ({ jobID }) => {
    const [outputs, setOutputs] = useState([
        new HistoryItem('comment', "./", "index.js", false),
        new HistoryItem('comment', "./", "index.js", true),
        new HistoryItem('test', "./", "index.js", false),
        new HistoryItem('test', "./", "index.js", true),
    ]);
 
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
    }, [outputs]);

    return (
        <div
            id='mock-terminal'
            className='bg-gray-950 custom-height font-mono overflow-auto p-4 text-green-400 text-sm w-full space-y-2'
            style={{ height: '700px' }}>
            {outputs.map((item, index) => (
                <HistoryRow key={index} item={item}></HistoryRow>
            ))}
        </div>
    );
};

export default History;
