import axios from 'axios';
import { api_endpoint } from '../../../api_endpoint';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { fileName } = req.body;

    if (!fileName) {
      return res.status(400).json({ error: 'File name is required' });
    }

    try {
      const response = await axios.post(api_endpoint + '/api/get_file', {
        file: fileName
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      return res.status(200).json(response.data);
    } catch (error) {
      console.error('Error fetching file:', error.response ? error.response.data : error.message);
      return res.status(error.response ? error.response.status : 500).json({
        error: error.response ? error.response.data : 'An error occurred while fetching the file'
      });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}