'use client';
import React, { useEffect } from 'react';
import { useState } from 'react';
// import ChatInterface from '../../components/chat/Chat';

import WorkspaceComponent from '../../components/workspace-components/WorkspaceComponents';
import Terminal from '../../components/terminal/Terminal';

const CodeNinja = () => {
  // const [isInitialized, setIsInitialized] = React.useState(true);
  const [jobID, setJobID] = useState('');
  const [fileSelectedPath, setFileSelectedPath] = useState(undefined);
  const [files, setFiles] = useState([])


  return (
    <div className='bg-gray-900 flex flex-col w-screen h-screen text-white'>
      <div className='flex w-full h-full mx-auto p-4'>
        <div className='pr-2 w-1/4'>
          <WorkspaceComponent jobID={jobID} fileSelectedPath={fileSelectedPath} setFileSelectedPath={setFileSelectedPath} files={files} setFiles={setFiles}/>
        </div>
        <div className='pl-2 w-3/4'>
          <Terminal jobID={jobID} fileSelectedPath={fileSelectedPath}/>
        </div>
      </div>
    </div>
  );
};

export default CodeNinja;
