import React, { useState, useEffect, CSSProperties } from 'react'
import ClockLoader from 'react-spinners/ClockLoader'
import PulseLoader from 'react-spinners/PulseLoader'
import FadeLoader from 'react-spinners/FadeLoader'
import { HistoryItem } from './HistoryItem'
import { FaAlignLeft } from 'react-icons/fa'
import { SiSpeedtest } from 'react-icons/si'
import { MdOutlineDone, MdEdit, MdOutlineClose } from 'react-icons/md'

const override = {
  display: 'block',
  margin: '0 auto',
  borderColor: 'white',
}

const HistoryRow = ({ item }) => {
  let [loading, setLoading] = useState(false)
  let [color, setColor] = useState('#FDFCDC')

  // Use useEffect to update loading state when item.loading changes
  useEffect(() => {
    setLoading(item.inProgress)
  }, [item.inProgress])

  return (
    <>
      {['test', 'comment', 'edit'].includes(item.type) ? (
        <div className='p-2 flex items-center border-2 rounded-lg border-[#FDFCDC] border-opacity-50 flex text-[#FDFCDC]'>
          <div>
            <div className='flex overflow-hidden items-center space-x-2'>
              <div className={item.type === 'comment' ? 'text-teal-600' : 'text-blue-500'}>
                {item.type === 'comment' && <FaAlignLeft />}
                {item.type === 'test' && <SiSpeedtest />}
                {item.type === 'edit' && <MdEdit />}
              </div>

              {item.type === 'test' && (
                <div className='py-1 truncates'>Generating and testing {item.pathFileName}</div>
              )}
              {item.type === 'comment' && (
                <div className='py-1 truncates'>Commenting {item.pathFileName}</div>
              )}
              {item.type === 'generate' && (
                <div className='py-1 truncates'>Generate test for {item.functionName} in {item.pathFileName}</div>
              )}
              {item.type === 'edit' && (
                <div className='py-1 truncates'>{item.pathFileName} edited in PR</div>
              )}
            </div>

            <span className='text-xs text-gray-500'>{item.timeStamp}</span>
          </div>

          <div className={`ml-auto ml-2 flex-shrink-0 ${loading ? 'w-6' : 'w-6'}`}>
            {loading ? (
              <ClockLoader
                color={color}
                loading={loading}
                cssOverride={override}
                size={20}
                aria-label='Loading Spinner'
                data-testid='loader'
              />
            ) : (
              <>
                {
                  item.failed ? <MdOutlineClose size={20} className='text-red-200' />
                    : <MdOutlineDone size={20} className='text-green-200' />
                }
              </>
            )}
            {/* <FadeLoader
                color={color}
                loading={loading}
                width={5}
                height={15}
                radius={2}
                aria-label="Loading Spinner"
                data-testid="loader"
              /> */}
          </div>
        </div>
      ) : (
        <div className='text-xs px-1 flex items-center text-[#FDFCDC]'>
          <div className='flex-grow overflow-hidden'>
            <div className={`py-1 truncates ${item.key === "running_test_ninja_update" && "text-orange-400"}`}>
              {item.description}
            </div>
            <span className='text-xs text-gray-500'>{item.timeStamp}</span>
          </div>

          <div className={`ml-2 flex-shrink-0 ${loading ? 'w-6' : 'w-6'}`}>
            {loading ? (
              <PulseLoader
                color={color}
                loading={loading}
                cssOverride={override}
                size={4}
                aria-label='Loading Spinner'
                data-testid='loader'
              />
            ) : (
              <>
                {
                  item.failed ? <MdOutlineClose size={20} className='text-red-200' />
                    : <MdOutlineDone size={20} className='text-green-200' />
                }
              </>
            )}
          </div>
        </div>
      )}
    </>
  )
}

export default HistoryRow
