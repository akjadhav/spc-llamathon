import React, { useState, useEffect } from 'react'
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs'
import { FaTerminal, FaFile } from 'react-icons/fa'
import { FaFileLines } from 'react-icons/fa6'
import Terminal from '../terminal/Terminal'
import History from '../history/History'
import Files from '../files/Files'
import { VscSparkleFilled, VscCircleFilled } from 'react-icons/vsc'
import { FaRobot, FaUser } from 'react-icons/fa'
import { Pill } from '@thumbtack/thumbprint-react'

const WorkspaceComponent = ({ fileSelectedPath, setFileSelectedPath, files, setFiles }) => {
  const [status, setStatus] = useState('')

  useEffect(() => {
    const fetchAgentStatus = async () => {
      try {
        const response = await fetch('/api/status')
        var jsonData = await response.json()

        const status = jsonData.data
        setStatus(status.toUpperCase())
      } catch (error) {
        // console.error('Failed to fetch data:', error);
      }
    }

    fetchAgentStatus()
    const intervalId = setInterval(fetchAgentStatus, 2000)

    return () => clearInterval(intervalId)
  }, [])

  return (
    <Tabs className='h-full max-h-screen flex flex-col bg-gray-950'>
      <TabList className='border-neutral-600 flex pb-1 bg-gray-900'>
        <Tab
          className='border-transparent cursor-pointer flex focus:outline-none hover:border-gray-300 hover:text-gray-600 items-center px-4 py-2 space-x-2 text-md'
          selectedClassName='bg-white text-black rounded-lg'
        >
          <FaTerminal className='text-lg' />
          <span>History</span>
        </Tab>
        <Tab
          className='border-b-2 border-transparent cursor-pointer flex focus:outline-none hover:border-gray-300 hover:text-gray-600 items-center px-4 py-2 space-x-2 text-md'
          selectedClassName='bg-white text-black rounded-lg'
        >
          <FaFileLines className='text-lg' />
          <span>Files</span>
        </Tab>
      </TabList>
      <div>
        <div className='border-b w-full border-neutral-600 flex gap-2 justify-end items-center px-2 py-2 text-md'>
          <VscSparkleFilled />
          {/* Chat */}
          {status === 'RUNNING' && (
            <Pill color='yellow' icon={<VscCircleFilled />}>
              Working
            </Pill>
          )}
          {status === 'COMPLETE' && (
            <Pill color='green' icon={<VscCircleFilled />}>
              Completed
            </Pill>
          )}
          {status === 'ONLINE' && (
            <Pill color='blue' icon={<VscCircleFilled />}>
              Online
            </Pill>
          )}
          {status === 'ERROR' && (
            <Pill color='red' icon={<VscCircleFilled />}>
              Error
            </Pill>
          )}
        </div>
      </div>

      <TabPanel>
        <History files={files} setFiles={setFiles} setFileSelectedPath={setFileSelectedPath} />
      </TabPanel>
      <TabPanel>
        <Files
          fileSelectedPath={fileSelectedPath}
          setFileSelectedPath={setFileSelectedPath}
          files={files}
          setFiles={setFiles}
        />
      </TabPanel>
    </Tabs>
  )
}

export default WorkspaceComponent
