const API_URL = 'http://localhost:8000';

function httpApiCall(method, path) {
    return async () => {
        const requestOptions = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${window.localStorage.getItem('access')}`
            }
        };
        const response = await fetch(`${API_URL}/${path}`, requestOptions);
        return response.json()
    }
}

export const httpGetUser = httpApiCall('GET', 'users/current/');
export const httpGetPhases = httpApiCall('GET', 'schedules/assessment-phases/');
