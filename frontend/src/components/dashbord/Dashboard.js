import React from 'react';
import PhaseHeader from "../pageHeader/phaseHeader";
import WindowTabs from "../tabs/WindowTabs";

const _ = require('lodash');

const Dashboard = ({ currentPhase }) => {
    return (
        <>
            { !_.isEmpty(currentPhase) &&
                <PhaseHeader currentPhase={currentPhase}/> }
        </>
    )
};

export default Dashboard;