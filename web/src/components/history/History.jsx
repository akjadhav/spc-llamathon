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

    console.log('HEHREHEHHHEH')

    useEffect(() => {
        const fetchData = async () => {
            try {
                console.log('Fetching data...')
                const response = await fetch('http://bb4f-67-188-146-74.ngrok-free.app/api/update')

                // Check if response is ok before parsing JSON
                if (!response.ok) {
                    const errorData = await response.json()
                    console.error(errorData.error)
                    return
                }

                const data = await response.json()
                console.log(data)
            } catch (err) {
                console.error('An error occurred while fetching data.')
                console.error(err) // Log the error itself instead of response
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
