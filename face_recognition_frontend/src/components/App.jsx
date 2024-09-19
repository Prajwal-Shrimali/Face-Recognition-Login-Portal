import './App.css';
import { useState } from 'react';
import axios from 'axios';

function App() {
  const [username, setUsername] = useState('');
  const [buttonColor, setButtonColor] = useState('#4CAF50'); 
  const [stateOfButton, setSetOfButton] = useState('Login')

  const handleLogin = async () => {
    setButtonColor('#FFC107');
    setSetOfButton('Authenticating...')

    // Immediately revert to the original color
    setTimeout(() => setButtonColor('#4CAF50'), 100);

    try {
      const response = await axios.post(
        'http://localhost:5000/login',
        { username },
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      console.log('Response:', response.data);
    } catch (error) {
      console.error('There was an error!', error.response ? error.response.data : error.message);
    }

    setSetOfButton('Login')
  };

  return (
    <div className="App">
      <div className='loginPart'>
        <h1>Face Recognition Software Authentication Portal</h1>
        <input
          type="text"
          placeholder="Enter Username"
          className="inputField"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <button
          onClick={handleLogin}
          className="loginButton"
          style={{ backgroundColor: buttonColor }}  // Dynamically set the button's background color
        >
          {stateOfButton}
        </button>
      </div>
    </div>
  );
}

export default App;
