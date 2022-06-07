import React, {useState} from 'react';
import './App.css';
import 'antd/dist/antd.css';
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import LogIn from './pages/login/LogIn';
import Portal from './pages/portal/Portal';

const App = () => {
    const homeUrl = process.env.NODE_ENV === 'production'
    ? 'https://examsched-rbnh6rv7hq-ey.a.run.app'
    : 'http://localhost:8000';

    const [requestUrl, setRequestUrl] = useState(homeUrl);

    if (!requestUrl) {
        setRequestUrl(homeUrl)
    }

    const refreshRequestBody = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            refresh: window.localStorage.getItem('refresh')
        })
    };

    return (
        <Router>
            <Routes>
                <Route path={'/login'} element={
                    <LogIn
                        requestUrl={requestUrl}
                    />
                }/>
                <Route path={'/'} element={
                    <LogIn
                        requestUrl={requestUrl}
                    />
                }/>
                <Route path={''} element={
                    <LogIn
                        requestUrl={requestUrl}
                    />
                }/>
                <Route path='/portal' element={
                    <Portal
                        requestUrl={requestUrl}
                        refreshRequestBody={refreshRequestBody}
                    />
                }/>
            </Routes>
        </Router>
    );
};

export default App;
