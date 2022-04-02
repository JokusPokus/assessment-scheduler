import React from 'react';
import {PageHeader, Button, Descriptions} from 'antd';
import './PhaseHeader.css';
import WindowTabs from "../tabs/WindowTabs";

const PhaseHeader = ({currentPhase, onWindowCreate}) => {
    return (
        <PageHeader
            className="phase-header"
            ghost={false}
        >
            <WindowTabs
                currentPhase={currentPhase}
                onWindowCreate={onWindowCreate}
            />
        </PageHeader>
    );
};

export default PhaseHeader;
