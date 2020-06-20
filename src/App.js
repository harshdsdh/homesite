import React from 'react';
import {Link} from 'react-router-dom'
import TwitterProject from './projects/twitter'
function App() {
  return (
    <div className="App">
      <h1>
        My Social Media POC 
      </h1>
      <ul>
        <li><Link to='/TwitterProject' target="_blank">twitter project</Link></li>
      </ul>
    </div>
  );
}

export default App;
