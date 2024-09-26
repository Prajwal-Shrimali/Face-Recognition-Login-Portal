import './App.css';
import { useState, useRef } from 'react';
import axios from 'axios';
import Modal from 'react-modal';
import crossImg from '../assets/cross.png';
import checkedImg from '../assets/checked.png';

Modal.setAppElement('#root'); // Set the root element for accessibility

function App() {
  const [username, setUsername] = useState('');
  const [buttonColor, setButtonColor] = useState('#4CAF50');
  const [stateOfButton, setStateOfButton] = useState('Login');
  const [authMessage, setAuthMessage] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loginURL, setLoginURL] = useState('');
  const videoRef = useRef(null);

  const startVideo = () => {
    return navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        videoRef.current.srcObject = stream;
        videoRef.current.style.display = 'block';
        return stream;
      })
      .catch((err) => console.error('Error accessing webcam: ', err));
  };

  const stopVideo = () => {
    const stream = videoRef.current.srcObject;
    const tracks = stream.getTracks();
    tracks.forEach(track => track.stop());
    videoRef.current.srcObject = null;
    videoRef.current.style.display = 'none';
  };

  const captureFrame = () => {
    const video = videoRef.current;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg');
  };

  const handleLogin = async () => {
    setButtonColor('#FFC107');
    setStateOfButton('Authenticating...');

    const stream = await startVideo();
    const frames = [];

    // Capture frames for 3 seconds in the background
    const captureInterval = setInterval(() => {
      const frame = captureFrame();
      frames.push(frame);
    }, 100);  // Capture a frame every 100ms

    setTimeout(() => {
      clearInterval(captureInterval);  // Stop capturing frames after 3 seconds
      stopVideo();  // Stop the video stream
      sendFramesToServer(frames);  // Send frames to the server to create the video
    }, 3000);  // Capture for 3 seconds
  };

  // const sendFramesToServer = async (frames) => {
  //   try {
  //     const response = await axios.post(
  //       'http://localhost:5000/login',
  //       { username, frames },  // Send the captured frames and username to the server
  //       {
  //         headers: {
  //           'Content-Type': 'application/json',
  //         },
  //       }
  //     );
  //     console.log('Response:', response.data);
  //     setAuthMessage(`Authentication Successful for user ${username}`);
  //     setLoginURL(response.data.loginURL);
  //   } catch (error) {
  //     console.error('There was an error!', error.response ? error.response.data : error.message);
  //     setAuthMessage('Authentication failed. Please try again.');
  //   }

  //   setButtonColor('#4CAF50');
  //   setStateOfButton('Login');
  //   setIsModalOpen(true); // Open the modal with the result
  // };

  const sendFramesToServer = async (frames) => {
    try {
      const response = await axios.post(
        'http://localhost:5000/login',
        { username, frames },  // Send the captured frames and username to the server
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      console.log('Response:', response.data);

      if (response.status === 200) {
        const { loginURL } = response.data; // Extract the login URL from the response
        setLoginURL(loginURL);
        setAuthMessage(`Authentication Successful for user ${username}`);
      } else {
        setAuthMessage(response.data.message || 'Authentication failed. Please try again.');
      }
    } catch (error) {
      console.error('There was an error!', error.response ? error.response.data : error.message);
      setAuthMessage('Authentication failed. Please try again.');
    }

    setButtonColor('#4CAF50');
    setStateOfButton('Login');
    setIsModalOpen(true); // Open the modal with the result
  };


  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <div className="App">
      <div className="loginPart">
        <h1>Face Recognition Software Authentication Portal</h1>
        <input
          type="text"
          placeholder="Enter Username"
          className="inputField"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <video ref={videoRef} autoPlay className="videoFeed" style={{ display: 'none' }}></video>
        <button
          onClick={handleLogin}
          className="loginButton"
          style={{ backgroundColor: buttonColor }}
        >
          {stateOfButton}
        </button>
      </div>

      <Modal isOpen={isModalOpen} onRequestClose={closeModal}>
        <div className='imageContainer'>
          {authMessage.startsWith('Authentication Successful') ? (
            <img src={checkedImg} alt="Success" className='authImage' />
          ) : (
            <img src={crossImg} alt="Failure" className='authImage' />
          )}
        </div>
        <h2>Authentication Result</h2>
        <p>{authMessage}</p>
        <Modal isOpen={isModalOpen} onRequestClose={closeModal}>
          <div className='imageContainer'>
            {authMessage.startsWith('Authentication Successful') ? (
              <img src={checkedImg} alt="Success" className='authImage' />
            ) : (
              <img src={crossImg} alt="Failure" className='authImage' />
            )}
          </div>
          <h2>Authentication Result</h2>
          <p>{authMessage}</p>

          {authMessage.startsWith('Authentication Successful') && loginURL ? (
            <a href={loginURL} target="_blank" rel="noopener noreferrer">
              <button>Open IAM USER {username}</button>
            </a>
          ) : null}

          <button onClick={closeModal}>Close</button>
        </Modal>

        <button onClick={closeModal}>Close</button>
      </Modal>
    </div>
  );
}

export default App;