import React from 'react';
import StaffTable from "./StaffTable";


const AssessorDashboard = ({window, windowStep, setWindowStep, setPhaseData}) => {
    return (
        <StaffTable
            window={window}
            windowStep={windowStep}
            setWindowStep={setWindowStep}
            apiResourceName={'assessors'}
            extensible={false}
            setPhaseData={setPhaseData}
        />
    )
};

export default AssessorDashboard;