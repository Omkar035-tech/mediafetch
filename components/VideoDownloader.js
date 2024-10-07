'use client'
import React, { useState } from 'react';
import axios from 'axios';

const VideoDownloader = () => {
    const [videoURL, setVideoURL] = useState('');
    const [formatId, setFormatId] = useState('18');

    const downloadVideo = async () => {
        try {
            console.log('Requesting video download with URL:', videoURL, 'and format id:', formatId);

            const response = await axios.get(`http://localhost:8000/download`, {
                params: { url: videoURL, format_id: formatId },
                responseType: 'blob', // Important to handle file download
            });
            console.log(response.data)
            const downloadUrl = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.setAttribute('download', `${videoURL.split('v=')[1]}.mp4`); // Extracting the video ID for naming
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            console.error('Error downloading video:', error);
            const errorMessage = error.response ? error.response.data.detail : "Unknown error occurred.";
            alert('Failed to download video: ' + errorMessage);
        }
    };

    return (
        <div className='px-4 sm:px-[5vw] md:px-[7vw] lg:px-[9vw]'>
            <h1>Download YouTube Video</h1>
            <input
                type="text"
                value={videoURL}
                onChange={(e) => setVideoURL(e.target.value)}
                placeholder="Enter YouTube video URL"
            />
            <br />
            <label>Select Quality:</label>
            <select value={formatId} onChange={(e) => setQuality(e.target.value)}>
                <option value="360p">360p</option>
                <option value="720p">720p</option>
                <option value="1080p">1080p</option>
            </select>
            <br />
            <button onClick={downloadVideo}>Download Video</button>
        </div>
    );
};

export default VideoDownloader;
