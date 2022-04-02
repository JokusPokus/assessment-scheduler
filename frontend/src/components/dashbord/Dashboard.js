import React, {useState, useEffect} from 'react';
import PhaseHeader from "../pageHeader/phaseHeader";
import {Skeleton} from "antd";
import WindowAdder from "./WindowAdder";

const _ = require('lodash');

const Dashboard = ({currentPhase}) => {
    const [activeComponent, setActiveComponent] = useState(
        <Skeleton active/>
    );

    useEffect(() => {
        if (!_.isEmpty(currentPhase)) {
            setActiveComponent(
                currentPhase.windows.length === 0
                    ? <WindowAdder currentPhase={currentPhase} />
                    : <PhaseHeader currentPhase={currentPhase} />
            );
        }
    }, [currentPhase]);

    return ( activeComponent )
};

export default Dashboard;