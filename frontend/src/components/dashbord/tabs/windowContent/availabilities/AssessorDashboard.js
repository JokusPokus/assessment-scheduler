import React from 'react';
import StaffTable from "./StaffTable";


const AssessorDashboard = ({window, windowStep, setWindowStep}) => {
    return (
        <StaffTable
            window={window}
            windowStep={windowStep}
            setWindowStep={setWindowStep}
            apiResourceName={'assessors'}
            extensible={false}
        />
    )
};

export default AssessorDashboard;