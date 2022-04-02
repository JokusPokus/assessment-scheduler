import React from 'react';
import {PageHeader, Button, Descriptions} from 'antd';
import './PhaseHeader.css';
import WindowTabs from "../tabs/WindowTabs";

const PhaseHeader = ({currentPhase}) => {
    return (
        <PageHeader
            className="phase-header"
            ghost={false}
        >
            <WindowTabs />
        </PageHeader>
    );
};

export default PhaseHeader;
