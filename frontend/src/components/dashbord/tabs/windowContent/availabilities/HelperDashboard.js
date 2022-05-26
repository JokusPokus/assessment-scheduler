import React from 'react';
import './HelperDashboard.css'
import StaffTable from "./StaffTable";


const HelperDashboard = ({window, windowStep, setWindowStep, setPhaseData}) => {
    return (
        <StaffTable
            window={window}
            windowStep={windowStep}
            setWindowStep={setWindowStep}
            apiResourceName={'helpers'}
            extensible={true}
            setPhaseData={setPhaseData}
        />
    )
};

export default HelperDashboard;
