import React from 'react';
import './HelperDashboard.css'
import StaffTable from "./StaffTable";


const HelperDashboard = ({window, windowStep, setWindowStep}) => {
    return (
        <StaffTable
            window={window}
            windowStep={windowStep}
            setWindowStep={setWindowStep}
            apiResourceName={'helpers'}
            extensible={true}
        />
    )
};

export default HelperDashboard;
