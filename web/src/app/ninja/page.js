'use client';
import React, { useEffect } from 'react';
import { useState } from 'react';
// import ChatInterface from '../../components/chat/Chat';

import WorkspaceComponent from '../../components/workspace-components/WorkspaceComponents';
import Terminal from '../../components/terminal/Terminal';

const CodeNinja = () => {
  // const [isInitialized, setIsInitialized] = React.useState(true);
  const [jobID, setJobID] = useState('');
  const [status, setStatus] = useState('');

  // useEffect(() => {
  //   const fetchAgentStatus = async () => {
  //     try {
  //       const response = await fetch(api_endpoint + '/' + jobID + '/status');
  //       var jsonData = await response.json();

  //       const status = jsonData.status;
  //       setStatus(status);
  //     } catch (error) {
  //       // console.error('Failed to fetch data:', error);
  //     }
  //   };

  //   fetchAgentStatus();
  //   const intervalId = setInterval(fetchAgentStatus, 1000);

  //   return () => clearInterval(intervalId);
  // }, [jobID]);

  return (
    <div className='bg-gray-900 flex flex-col w-screen h-screen text-white'>
      <div className='flex w-full h-full mx-auto p-4'>
        <div className='pr-2 w-1/4'>
          <WorkspaceComponent jobID={jobID} />
        </div>
        <div className='pl-2 w-3/4'>
          <Terminal jobID={jobID} />
        </div>
      </div>
    </div>
  );
};

export default CodeNinja;
