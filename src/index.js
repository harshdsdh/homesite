import React from 'react';
import ReactDOM from 'react-dom';
import TwitterProject from './projects/twitter'
import {Route, BrowserRouter as Router} from 'react-router-dom'
import App from './App';
import * as serviceWorker from './serviceWorker';

const routing=(
  <Router>
    <div id='routing-container'>
    <Route path='/home' component ={App}></Route>
      <Route path='/TwitterProject' component ={TwitterProject}></Route>
    </div>
  </Router>
)

ReactDOM.render(
 routing,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
