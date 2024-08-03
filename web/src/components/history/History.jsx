import React, { useState, useEffect, use } from 'react'
import { api_endpoint } from '../../api_endpoint'
import HistoryRow from './HistoryRow'
import HistoryItem from './HistoryItem'

const History = ({ jobID }) => {
    const [outputs, setOutputs] = useState([
        new HistoryItem('text', "./", "index.js", "Git Pull Request dectected", true),
        new HistoryItem('text', './', 'index.js', 'Agent is live...', false),
        new HistoryItem('comment', './', 'index.js'),
        new HistoryItem('comment', './', 'index.js', '', true),
        new HistoryItem('test', './', 'index.js'),
        new HistoryItem('test', './', 'index.js', '', true),
    ])
    useEffect(() => {
        const fetchData = async () => {
            const requestOptions = {
                method: "GET",
                redirect: "follow"
            };

            try {
                const response = await fetch("http://127.0.0.1:5002/api/update", requestOptions);
                const result = await response.text();
                console.log(result);
            } catch (error) {
                console.error(error);
            }
        }

        fetchData()

        const intervalId = setInterval(fetchData, 10000)

        return () => clearInterval(intervalId)
    }, [])

    // Effect to make sure the terminal is scrolled to the bottom on new output
    useEffect(() => {
        const terminal = document.getElementById('mock-terminal')
        if (terminal) {
            terminal.scrollTop = terminal.scrollHeight
        }
    }, [outputs])

    return (
        <div
            id='mock-terminal'
            className='bg-gray-950 custom-height font-mono overflow-auto p-4 text-green-400 text-sm w-full space-y-2'
            style={{ height: '700px' }}
        >
            {outputs.map((item, index) => (
                <HistoryRow key={index} item={item}></HistoryRow>
            ))}
        </div>
    )
}

export default History
