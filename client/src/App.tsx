import React, { useState } from 'react'
import './App.css'


function App() {
  const [image, setImage] = useState<File | null>(null)
  const [model, setModel] = useState<string | null>(null);
  const [prediction, setPrediction] = useState<string | null>(null);

  const handleFileChoose = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setImage(e.target.files[0]);
    }
  }

  const startCamera = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    const videoElement = document.getElementById('video') as HTMLVideoElement;
    if (videoElement) {
      videoElement.srcObject = stream;
      videoElement.play();
    }
  };

  const captureFrame = () => {
    const canvas = document.createElement('canvas');
    const video = document.getElementById('video') as HTMLVideoElement;

    if (video) {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const context = canvas.getContext('2d');
      if (context) {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const frame = canvas.toDataURL('image/png');
        return frame;
      }
    }
    return null;
  };

  const handleModelChoose = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedModel(e.target.value);
  }
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!image && !captureFrame()) {
      alert("Select an Image or Capture a Frame");
      return;
    }

    if (!model) {
      alert("Select a Model");
      return;
    }




    const formData = new FormData();
    if (image) {
      formData.append("image_file", image);
    } else {
      const frame = captureFrame();
      if (frame) {
        const blob = await fetch(frame).then(res => res.blob());
        formData.append("image_file", blob, "frame.png");
      }
    }
    formData.append("model", model)

    try {
      const response = await fetch(`${import.meta.env.VITE_SERVER_LOCATION}/predict/`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        alert(`Error: ${errorData.error}`);
        return;
      }

      const data = await response.json();

      setPrediction(data.result);
    } catch (error) {
      console.error(error);
    }

  }
  const setSelectedModel = (value: string) => {
    setModel(value)
  }

  return (
    <>
      <form onSubmit={handleSubmit} encType="multipart/form-data">
        <input type="file" name="image_file" onChange={handleFileChoose} />
        <select onChange={handleModelChoose}>
          <option value="">Select a Model</option>
          <option value="Deep Neural Network">Deep Neural Network</option>
          <option value="Resnet 152">Resnet 152</option>
        </select>
        <button type="submit">Predict</button>
      </form>

      <button onClick={startCamera}>Start Camera</button>
      <video id="video" style={{ width: '50%', height: 'auto' }} autoPlay muted></video>
      <button type="button" onClick={captureFrame}>Capture Frame</button>

      {prediction && <h3>Prediction: {prediction}</h3>}
    </>
  )
}

export default App
