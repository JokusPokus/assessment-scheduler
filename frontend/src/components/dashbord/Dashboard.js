import React, {useState, useEffect} from 'react';
import PhaseHeader from "../pageHeader/phaseHeader";
import {Skeleton} from "antd";
import WindowAdder from "./WindowAdder";
import {httpPostWindow} from "../../hooks/requests";

const _ = require('lodash');

const Dashboard = ({currentPhase, newWindowCounter, setNewWindowCounter}) => {
    const [activeComponent, setActiveComponent] = useState(
        <Skeleton active/>
    );

    const onWindowCreate = async (values) => {
        const requestBody = {
            start_date: values.timeFrame[0].format('YYYY-MM-DD'),
            end_date: values.timeFrame[1].format('YYYY-MM-DD'),
            block_length: values.blockLength,
            assessment_phase: currentPhase.id
        };
        await httpPostWindow(requestBody)();
        setNewWindowCounter(newWindowCounter + 1);
    };

    useEffect(() => {
        if (!_.isEmpty(currentPhase)) {
            setActiveComponent(
                currentPhase.windows.length === 0
                    ? <WindowAdder onWindowCreate={onWindowCreate} />
                    : <PhaseHeader currentPhase={currentPhase} onWindowCreate={onWindowCreate} />
            );
        }
    }, [currentPhase]);

    return (activeComponent)
};

export default Dashboard;