'use client';
import React from 'react';
import { Inter } from 'next/font/google';
import Head from 'next/head';
import Icon from './icon.png'
import Image from "next/image";

const inter = Inter({ subsets: ['latin'] });

export default function Home() {
  return (
    <>
      <Head>
        <style>{`
          @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
          }
          @keyframes gradient-animation {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
          }
          @keyframes float {
            0% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
            100% { transform: translateY(0); }
          }
          @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
      </Head>
      <div className='bg-black h-screen overflow-hidden relative'>
        <div className='absolute h-full left-0 top-0 w-full'>
          <div
            className='absolute animate-gradient-animation bg-gradient-to-r bg-gray-900 h-full left-0 opacity-40 to-blue-500 top-0 via-indigo-500 w-full'
            style={{
              backgroundSize: '200% 200%',
              animation: 'gradient-animation 10s ease infinite',
            }}></div>
        </div>
        <div className='flex flex-col h-full items-center justify-center relative z-10'>
          <div className='relative text-center flex flex-col items-center justify-center'>
            <div className='w-full flex justify-center pb-5'>
              <Image src={Icon} alt='Icon' className='mr-2 w-32 h-32' />
            </div>
            <h1 className='mb-8 text-6xl text-white chakra-petch-semibold'>TestNinja.</h1>

            <button
              className='animate-pulse bg-white duration-300 ease-in-out font-semibold hover:bg-gray-200 px-8 py-4 rounded-full shadow-lg text-black transition'
              onClick={() => {
                window.location.href = '/ninja';
              }}
              style={{ animation: 'pulse 2s infinite' }}>
              Experience
            </button>
          </div>

        </div>
      </div>
    </>
  );
}
