import { NextResponse } from 'next/server';

const POLL_DURATION = 10000; // Poll for 10 seconds
const POLL_INTERVAL = 1000; // Poll every 1 second

export async function GET(request) {
  try {
    const results = await pollData();
    return NextResponse.json(
      { data: results, status: 200 },
    );
  } catch (error) {
    console.error('Error in GET handler:', error);
    return NextResponse.json(
      { data: {}, error: error.message, status: 500 },
    );
  }
}

async function pollData() {
  const startTime = Date.now();
  const results = [];

  while (Date.now() - startTime < POLL_DURATION) {
    try {
      const result = await fetchData();
      results.push(result);
    } catch (error) {
      console.error('Error fetching data:', error);
    }

    // Wait for the next interval
    await new Promise(resolve => setTimeout(resolve, POLL_INTERVAL));
  }

  return results;
}

async function fetchData() {
  const requestOptions = {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'ngrok-skip-browser-warning': '69420',
    },
  };

  const response = await fetch(
    'https://bb4f-67-188-146-74.ngrok-free.app/api/update',
    requestOptions
  );

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const result = await response.json();
  return result;
}