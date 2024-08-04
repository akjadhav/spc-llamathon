import React, { useState, useEffect, use } from 'react'
import File from './File'
import FilesRow from './FilesRow'

const Files = ({ fileSelectedPath, setFileSelectedPath, files, setFiles }) => {
  // const [files, setFiles] = useState([
  //     new File("./", "index.js"),
  //     new File("./", "page.js"),
  // ]);

  return (
    <div className='h-full flex flex-col'>
      <div
        id='mock-terminal'
        className='bg-gray-950 font-mono overflow-auto text-green-400 text-sm space-y-2 h-full'
      >
        {files.map((file, index) => (
          <FilesRow
            key={index}
            file={file}
            fileSelectedPath={fileSelectedPath}
            setFileSelectedPath={setFileSelectedPath}
          />
        ))}
      </div>
    </div>
  )
}

export default Files
