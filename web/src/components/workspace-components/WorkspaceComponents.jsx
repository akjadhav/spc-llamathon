import React from 'react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import { FaTerminal, FaFile } from 'react-icons/fa';
import { FaFileLines } from "react-icons/fa6";
import Terminal from '../terminal/Terminal';
import History from '../history/History';
import Files from '../files/Files';

const WorkspaceComponent = ({ jobID }) => {
  return (
    <Tabs className='h-full flex flex-col bg-gray-950'>
      <TabList className='border-b border-neutral-600 flex pb-1 bg-gray-900'>
        <Tab
          className='border-b-2 border-transparent cursor-pointer flex focus:outline-none hover:border-gray-300 hover:text-gray-600 items-center px-4 py-2 space-x-2 text-md'
          selectedClassName='bg-white text-black rounded-lg'>
          <FaTerminal className='text-lg' />
          <span>History</span>
        </Tab>
        <Tab
          className='border-b-2 border-transparent cursor-pointer flex focus:outline-none hover:border-gray-300 hover:text-gray-600 items-center px-4 py-2 space-x-2 text-md'
          selectedClassName='bg-white text-black rounded-lg'>
          <FaFileLines className='text-lg' />
          <span>Files</span>
        </Tab>
      </TabList>
      <TabPanel>
        <History jobID={jobID} />
      </TabPanel>
      <TabPanel>
        <Files jobID={jobID} />
      </TabPanel>
    </Tabs>
  );
};

export default WorkspaceComponent;
