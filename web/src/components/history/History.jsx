import React, { useState, useEffect, useCallback } from 'react'
import HistoryRow from './HistoryRow'
import HistoryItem from './HistoryItem'

const History = ({ jobID, files, setFiles, setFileSelectedPath }) => {
  const [outputKeys, setOutputsKeys] = useState([])
  const [outputKeyToData, setOutputKeyToData] = useState({})


  const updateFiles = useCallback((newFiles) => {
    setFiles(prevFiles => {
      const uniqueFiles = [...new Set([...prevFiles, ...newFiles])]
      console.log('uniqueFiles', uniqueFiles)
      return uniqueFiles
    })
  }, [setFiles])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/update')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const result = await response.json()
        if (result.data && result.data instanceof Array) {
          const newOutputs = result.data.map((item) => new HistoryItem(
            item.key, item.type, item.pathFileName, item.timestamp,
            item.description, item.functionName, item.inProgress, item.failed
          ))

          setOutputKeyToData(prevOutputKeyToData => {
            const updatedOutputKeyToData = { ...prevOutputKeyToData }
            const newFiles = []
            let newKeysAdded = false

            for (const item of newOutputs) {
              if (item.key in prevOutputKeyToData) {
                updatedOutputKeyToData[item.key] = {
                  ...prevOutputKeyToData[item.key],
                  inProgress: item.inProgress,
                }
              } else {
                updatedOutputKeyToData[item.key] = item
                if (item.type !== 'text' && !item.inProgress) {
                  newFiles.push(item.pathFileName)
                }
                newKeysAdded = true
                if (item.type === 'test') {
                  setFileSelectedPath(item.pathFileName)
                }
              }
            }

            if (newKeysAdded) {
              setOutputsKeys(Object.keys(updatedOutputKeyToData))
              updateFiles(newFiles)
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
  }, [setFileSelectedPath, updateFiles])

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
      style={{ 'overflow-y': 'auto', height: '700px' }}
    >
      {outputKeys.map((key, index) => (
        <HistoryRow key={index} item={outputKeyToData[key]}></HistoryRow>
      ))}
    </div>
  )
}

export default History
