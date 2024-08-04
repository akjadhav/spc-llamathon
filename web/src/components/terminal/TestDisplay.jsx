import React, { useState, useEffect, CSSProperties } from 'react'
import { MdOutlineDone, MdEdit, MdOutlineClose } from 'react-icons/md'

const ListItem = ({ testName, passed }) => (
    <li className="flex items-center space-x-2 justify-between">
        <div className={`text-sm truncates ${passed ? "text-green-400" : "text-red-400"}`}>
            {testName}
        </div>

        {
            passed ? <MdOutlineDone size={20} className='text-green-400' />
                : <MdOutlineClose size={20} className='text-red-400' />
        }
    </li>
);

const TestDisplay = ({ testStatus }) => {
    return (
      <div className="absolute w-1/5 top-0 right-0 bg-gray-800 bg-opacity-80 p-2 rounded-lg shadow-lg mt-2 mr-2 max-h-1/3 flex flex-col">
        <span className="mb-2">
          Test Results
        </span>
        <div className='flex-grow space-y-2 overflow-y-auto'>
          {
            Object.keys(testStatus).map((suite, index) => {
              const suitTests = testStatus[suite];
              const countPasses = Object.values(suitTests).filter(test => test).length;
              const anyFails = countPasses < Object.keys(suitTests).length;
              return (
                <div key={index} className={`items-center space-x-2 ${anyFails ? "text-red-400" : "text-green-400"}`}>
                  <div className={`text-sm font-semibold justify-between flex `}>
                    <>{suite}</>
                    <span className='flex font-normal'>
                      ({countPasses}/{Object.keys(suitTests).length} passed)
                      <span className='pl-1'>
                        {
                          !anyFails ? <MdOutlineDone size={20} className='text-green-400' />
                            : <MdOutlineClose size={20} className='text-red-400' />
                        }
                      </span>
                    </span>
                  </div>
                  <div className='text-sm font-normal'>
                    {
                      Object.keys(suitTests).map((testName, index) => (
                        <ListItem key={index} testName={testName} passed={suitTests[testName]} />
                      ))
                    }
                  </div>
                </div>
              )
            })
          }
        </div>
      </div>
    )
  }
  
  export default TestDisplay