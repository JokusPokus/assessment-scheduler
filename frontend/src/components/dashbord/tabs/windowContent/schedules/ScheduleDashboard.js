import React from 'react';
import {Button} from "antd";
import {httpTriggerScheduling} from "../../../../../hooks/requests";


const ScheduleDashboard = ({window, windowStep, setWindowStep}) => {
    const triggerScheduling = async () => {
        await httpTriggerScheduling(window.id)();
    };

    return(
        <div className="fade-in">
            <Button onClick={triggerScheduling}>Trigger me!</Button>
        </div>
    )
};

export default ScheduleDashboard;
