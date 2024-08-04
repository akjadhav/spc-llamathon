'use client';
import React, { useEffect } from 'react';
import { useState } from 'react';
// import ChatInterface from '../../components/chat/Chat';

import WorkspaceComponent from '../../components/workspace-components/WorkspaceComponents';
import Terminal from '../../components/terminal/Terminal';
import Icon from '../../app/icon.png'
import Image from "next/image"; 

const TestNinja = () => {
  // const [isInitialized, setIsInitialized] = React.useState(true);
  const [jobID, setJobID] = useState('');
  const [fileSelectedPath, setFileSelectedPath] = useState(undefined);
  const [files, setFiles] = useState([])

  return (
    <div className='bg-gray-900 flex flex-col w-screen h-screen text-white'>
      <div className='px-6 pt-4 w-full'>
        <h1 className='font-bold text-4xl text-center text-blue-500 chakra-petch-semibold flex items-center justify-center'>
          <Image src={Icon} alt='Icon' className='mr-2 w-10 h-10' />
          <span className='text-white'>TestNinja</span>
        </h1>
      </div>


      <div className='flex w-full h-full mx-auto px-6 pt-2 pb-4 '>
        <div className='pr-2 w-1/4'>
          <WorkspaceComponent jobID={jobID} fileSelectedPath={fileSelectedPath} setFileSelectedPath={setFileSelectedPath} files={files} setFiles={setFiles} />
        </div>
        <div className='pl-2 w-3/4'>
          <Terminal jobID={jobID} fileSelectedPath={fileSelectedPath} />
        </div>
      </div>
    </div>
  );
};

export default TestNinja;
