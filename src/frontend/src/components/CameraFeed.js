import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';

const socket = io('http://localhost:3001');

function CameraFeed({ cameraId }){
    const [frames, setFrames] = useState([]);

    useEffect(()=> {
        socket.emit('join', cameraId);
        socket.on('frame', (frame) => {
            setFrames((prevFrames) => [...prevFrames,frame]);
        });
        
        return () => {
            socket.off('frame');
        };
    }, [cameraId]);

    return (
        <div className="camera-feed">
            {frames.map((frame,index) => (
                <img key={index} src={`data:image/jpeg;base64,${frame}`} alt="frame"/>
            ))}
        </div>
    );
}

export default CameraFeed;