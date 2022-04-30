import React from 'react';
import './HelperDashboard.css'
import StaffTable from "./StaffTable";


const HelperDashboard = ({window}) => {
    return (
        <StaffTable
            window={window}
            apiResourceName={'helpers'}
            extensible={true}
        />
    )
};

export default HelperDashboard;
