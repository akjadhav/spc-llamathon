import React, { useState, useEffect, use } from 'react'
import HistoryRow from './HistoryRow'
import HistoryItem from './HistoryItem'

const History = ({ jobID, files, setFiles }) => {
  //   const [outputs, setOutputs] = useState([
  //     new HistoryItem('text', './index.js', 'Git Pull Request dectected', true),
  //     new HistoryItem('text', './index.js', 'Agent is live...', false),
  //     new HistoryItem('comment', './index.js'),
  //     new HistoryItem('comment', './index.js', '', true),
  //     new HistoryItem('test', './index.js'),
  //     new HistoryItem('test', './index.js', '', true),
  //   ])

  const [outputKeys, setOutputsKeys] = useState([])
  const [outputKeyToData, setOutputKeyToData] = useState({})

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/update')

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const result = await response.json()

        if (result.data) {
          const newOutputs = result.data.map((item) => {
            return new HistoryItem(
              item.key,
              item.type,
              item.pathFileName,
              item.timestamp,
              item.description,
              item.inProgress,
            )
          })

          setOutputKeyToData((prevOutputKeyToData) => {
            const updatedOutputKeyToData = { ...prevOutputKeyToData }
            const updatedFiles = [...files]
            let newKeysAdded = false

            for (const item of newOutputs) {
              if (item.key in prevOutputKeyToData) {
                // Update only the inProgress field for existing items
                updatedOutputKeyToData[item.key] = {
                  ...prevOutputKeyToData[item.key],
                  inProgress: item.inProgress,
                }
              } else {
                // Add new item
                updatedOutputKeyToData[item.key] = item
                if (!item.inProgress) {
                  updatedFiles.push(item.pathFileName)
                }
                newKeysAdded = true
              }
            }

            if (newKeysAdded) {
              setOutputsKeys(Object.keys(updatedOutputKeyToData))
              // remove all duplicates
              const uniqueFiles = [...new Set(updatedFiles)]
              setFiles(uniqueFiles)
            }

            return updatedOutputKeyToData
          })
        }
      } catch (error) {
        console.error('Fetch error:', error)
      }
    }

    fetchData()

    const intervalId = setInterval(fetchData, 1500)

    return () => clearInterval(intervalId)
  }, [])

  // Effect to make sure the terminal is scrolled to the bottom on new output
  useEffect(() => {
    const terminal = document.getElementById('mock-terminal')
    if (terminal) {
      terminal.scrollTop = terminal.scrollHeight
    }
  }, [outputKeys])

  return (
    <div
      id='mock-terminal'
      className='bg-gray-950 custom-height font-mono overflow-auto p-4 text-green-400 text-sm w-full space-y-2'
      style={{ height: '700px' }}
    >
      {outputKeys.map((key, index) => (
        <HistoryRow key={index} item={outputKeyToData[key]}></HistoryRow>
      ))}
    </div>
  )
}

export default History
