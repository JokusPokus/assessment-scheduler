const _ = require("lodash");

const API_URL = process.env.NODE_ENV === 'production'
    ? 'https://examsched-rbnh6rv7hq-ey.a.run.app'
    : 'http://localhost:8000';

function httpApiCall(method, path, body) {
    return async () => {
        const requestOptions = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${window.localStorage.getItem('access')}`
            }
        };
        if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
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
export const httpPostModuleDurations = _.partial(httpApiCall, 'POST', 'exams/modules/add-durations/');

export const httpGetPhase = _.partial(
    httpGetResourceById, ({year, semester}) => {
        return `schedules/assessment-phases/${year}/${semester}/`
    });

export const httpPostBlockSlots = (windowId, body) => {
    const path = `schedules/windows/${windowId}/add-block-slots/`;
    return httpApiCall('POST', path, body);
};

export const httpGetStaff = (windowId, apiResourceName) => {
    const path = `staff/${apiResourceName}/?window=${windowId}`;
    return httpApiCall('GET', path, null);
};

export const httpGetModules = (windowId) => {
    const path = `exams/modules/?window=${windowId}`;
    return httpApiCall('GET', path, null);
};

export const httpGetSchedulingStatus = (windowId) => {
    const path = `schedules/windows/${windowId}/scheduling-status/`;
    return httpApiCall('GET', path, null);
};

export const httpGetScheduleEvaluation = (windowId) => {
    const path = `schedules/windows/${windowId}/schedule-evaluation/`;
    return httpApiCall('GET', path, null);
};

export const httpGetCSV = (windowId) => {
    const path = `schedules/windows/${windowId}/get-csv/`;
    return httpApiCall('GET', path, null);
};

export const httpPostStaffAvails = (windowId, body, apiResourceName) => {
    const path = `schedules/windows/${windowId}/add-staff-availabilities/?resource=${apiResourceName}`;
    return httpApiCall('POST', path, body);
};

export const httpDeleteHelper = (email, windowId) => {
    const path = `schedules/windows/${windowId}/remove-staff/`;
    const body = {email: email};
    return httpApiCall('DELETE', path, body)
};

export const httpDeleteWindow = (windowId) => {
    const path = `schedules/windows/${windowId}/`;
    return httpApiCall('DELETE', path, null)
};

export const httpPatchWindow = (windowId, body) => {
    const path = `schedules/windows/${windowId}/`;
    return httpApiCall('PATCH', path, body)
};

export const httpTriggerScheduling = (windowId) => {
    const path = `schedules/windows/${windowId}/trigger-scheduling`;
    return httpApiCall('GET', path, null);
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

