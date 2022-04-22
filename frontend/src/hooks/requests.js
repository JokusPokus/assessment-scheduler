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
        if (method === 'POST') {
            requestOptions['body'] = JSON.stringify(body)
        }
        return await fetch(`${API_URL}/${path}`, requestOptions);
    }
}


function httpGetResourceById(pathTemplate, resourceId) {
    const path = pathTemplate(resourceId);
    return httpApiCall('GET', path, null);
}


export const httpGetUser = httpApiCall('GET', 'users/current/', null);
export const httpGetPhases = httpApiCall('GET', 'schedules/assessment-phases/', null);
export const httpPostPhase = _.partial(httpApiCall, 'POST', 'schedules/assessment-phases/');
export const httpPostWindow = _.partial(httpApiCall, 'POST', 'schedules/windows/');

export const httpGetPhase = _.partial(
    httpGetResourceById, ({year, semester}) => {
        return `schedules/assessment-phases/${year}/${semester}/`
    });

export const httpPostBlockSlots = (windowId, body) => {
    const path = `schedules/windows/${windowId}/add-block-slots/`;
    return httpApiCall('POST', path, body);
};

export const httpPostPlanningSheet = async (body) => {
    const formData = new FormData();
    for (const key in body) {
        formData.append(key, body[key]);
    }

    const requestOptions = {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${window.localStorage.getItem('access')}`
        },
        body: formData
    };
    return await fetch(`${API_URL}/upload/planningSheet.csv/`, requestOptions);
};

