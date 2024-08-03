import React, { useState, useEffect, CSSProperties } from "react";
import ClockLoader from "react-spinners/ClockLoader";
import PulseLoader from "react-spinners/PulseLoader";
import FadeLoader from "react-spinners/FadeLoader";
import { HistoryItem } from './HistoryItem';
import { FaAlignLeft } from "react-icons/fa";
import { SiSpeedtest } from "react-icons/si";
import { MdOutlineDone } from "react-icons/md";

const override = {
  display: "block",
  margin: "0 auto",
  borderColor: "white",
};

const HistoryRow = ({ item }) => {
  let [loading, setLoading] = useState(false);
  let [color, setColor] = useState("#FDFCDC");

  // Use useEffect to update loading state when item.loading changes
  useEffect(() => {
    setLoading(item.inProgress);
  }, [item.inProgress]);

  return (
    <>
      {
        ["test", "comment"].includes(item.type) ?
          <div className='p-2 flex items-center border-2 rounded-lg border-[#FDFCDC] border-opacity-50 text-[#FDFCDC]'>
            <div className='flex items-center'>
              <div className={item.type === "comment" ? "text-teal-600" : "text-blue-500"}>
                {item.type === 'comment' ? <FaAlignLeft /> : <SiSpeedtest />}
              </div>

              <span className='text-md pl-2'>
                {item.path}{item.fileName}
              </span>
            </div>

            {loading && (
              <div className='ml-auto opacity-75'>
                <ClockLoader
                  color={color}
                  loading={loading}
                  cssOverride={override}
                  size={20}
                  aria-label="Loading Spinner"
                  data-testid="loader"
                />
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
            )}
          </div>
          :
          <div className='text-xs px-1 flex items-center text-[#FDFCDC]'>
            <div className='flex items-center py-1'>
              {item.description}
            </div>

            <div className={`ml-auto opacity-75 pr-1 ${loading && 'mt-1'}`}>
              {loading ? (
                <PulseLoader
                  color={color}
                  loading={loading}
                  cssOverride={override}
                  size={4}
                  aria-label="Loading Spinner"
                  data-testid="loader"
                />
              ) :
                <MdOutlineDone size={20} className="text-green-200"/>
              }
            </div>
          </div>
      }
    </>
  )
}

export default HistoryRow