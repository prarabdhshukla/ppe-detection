import React, { useState, useEffect } from 'react';
import CameraFeed from './components/CameraFeed';
import './App.css';

function App(){
    const [selectedCamera, setSelectedCamera] = useState(null);

    return (
        <div className="App">
            <h1>PPE Detection</h1>
            <div className="camera-selection">
                <button onClick={() => setSelectedCamera('camera1')}>Camera 1</button>
                <button onClick={() => setSelectedCamera('camera2')}>Camera 2</button>
            </div>
            {selectedCamera && <CameraFeed cameraId={selectedCamera}/>}
        </div>
    );
}

export default App;