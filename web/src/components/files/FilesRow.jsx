import React from "react";

const FilesRow = ({ file, index, fileSelectedPath, setFileSelectedPath }) => {
    return (
        <div className={`flex items-center text-[#FDFCDC] underline ${`${file}` === fileSelectedPath && 'bg-gray-700'} py-1 cursor-pointer`}
            onClick={() => {
                setFileSelectedPath(`${file}`);
            }}
        >
            <div className='flex items-center'>
                <span className='text-md pl-3'>
                    {file}
                </span>
            </div>

        </div>
    )
}

export default FilesRow