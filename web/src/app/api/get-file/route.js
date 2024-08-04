import { NextResponse } from 'next/server';
import axios from 'axios';
import { api_endpoint } from '../../../api_endpoint'; // Adjust this path as needed

export async function POST(req) {
  try {
    const body = await req.json();
    const { fileName } = body;

    if (!fileName) {
      return NextResponse.json({ error: 'File name is required' }, { status: 400 });
    }

    const response = await axios.post(`${api_endpoint}/api/get_file`, {
      fileName: fileName
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });

    return NextResponse.json(response.data);
  } catch (error) {
    console.error('Error fetching file:', error.response ? error.response.data : error.message);
    console.error('Full error object:', error);
    return NextResponse.json(
      { error: error.response ? error.response.data : 'An error occurred while fetching the file' },
      { status: error.response ? error.response.status : 500 }
    );
  }
}