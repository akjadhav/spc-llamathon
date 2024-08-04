import React from "react";

const FilesRow = ({ file, index, fileSelectedPath, setFileSelectedPath }) => {
    return (
        <div className={`flex items-center text-[#FDFCDC] underline ${`${file.path}${file.fileName}` === fileSelectedPath && 'bg-gray-700'} py-1 cursor-pointer`}
            onClick={() => {
                setFileSelectedPath(`${file.path}${file.fileName}`);
            }}
        >
            <div className='flex items-center'>
                <span className='text-md pl-3'>
                    {file.path}{file.fileName}
                </span>
            </div>

        </div>
    )
}

export default FilesRow