import React, { useState } from 'react';
import './App.css';
import 'antd/dist/antd.css';
import {BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from './pages/landingpage/LandingPage';

const App = () => {
  const [requestUrl, setRequestUrl] = useState('http://localhost:8000');

  if(!requestUrl) {
    setRequestUrl('http://localhost:8000')
  }

  const refreshRequestBody = {
    method: 'POST',
    headers : {
        'Content-Type': 'application/json',
    },
    body : JSON.stringify({
        refresh : window.localStorage.getItem('refresh')
    })
  };

  return (
    <Router>
      <Routes>
        <Route path='/' element={<LandingPage/>} />
      </Routes>
    </Router>
  );
};

export default App;
