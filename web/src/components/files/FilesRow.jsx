import React from "react";

const FilesRow = ({ file, index, fileSelectedIndex, setFileSelectedIndex }) => {
    return (
        <div className={`flex items-center text-[#FDFCDC] underline ${index === fileSelectedIndex && 'bg-gray-600'} py-1 cursor-pointer`}
            onClick={() => {
                setFileSelectedIndex(index);
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