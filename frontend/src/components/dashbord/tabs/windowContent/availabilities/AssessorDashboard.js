import React from 'react';
import StaffTable from "./StaffTable";


const AssessorDashboard = ({window}) => {
    return (
        <StaffTable
            window={window}
            apiResourceName={'assessors'}
            extensible={false}
        />
    )
};

export default AssessorDashboard;