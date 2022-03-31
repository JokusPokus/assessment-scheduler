const _ = require("lodash");

const API_URL = 'http://localhost:8000';

function httpApiCall(method, path, body) {
    return async () => {
        const requestOptions = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${window.localStorage.getItem('access')}`
            }
        };
        if (method==='POST') {
            requestOptions['body'] = JSON.stringify(body)
        }
        const response = await fetch(`${API_URL}/${path}`, requestOptions);
        return response.json()
    }
}

export const httpGetUser = httpApiCall('GET', 'users/current/', null);
export const httpGetPhases = httpApiCall('GET', 'schedules/assessment-phases/', null);
export const httpPostPhase = _.partial(httpApiCall, 'POST', 'schedules/assessment-phases/');