import React from 'react';
import {PageHeader, Button, Descriptions} from 'antd';
import './PhaseHeader.css';
import WindowTabs from "../tabs/WindowTabs";

const PhaseHeader = ({onWindowCreate}) => {
    return (
        <PageHeader
            className="phase-header"
            ghost={false}
        >
            <WindowTabs onWindowCreate={onWindowCreate} />
        </PageHeader>
    );
};

export default PhaseHeader;
