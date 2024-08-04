import { NextResponse } from 'next/server';

export async function GET(request) {
  try {
    const result = await fetchData();
    return NextResponse.json(
      { data: result, status: 200 },
    );
  } catch (error) {
    console.error('Error in GET handler:', error);
    return NextResponse.json(
      { data: {}, error: error.message, status: 500 },
    );
  }
}

async function fetchData() {
  const requestOptions = {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'ngrok-skip-browser-warning': '69420',
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0',
    },
  };

  // Add a timestamp to the URL to prevent caching
  const timestamp = new Date().getTime();
  const url = `https://bb4f-67-188-146-74.ngrok-free.app/api/status?t=${timestamp}`;

  const response = await fetch(url, requestOptions);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const result = await response.json();
  return result;
}