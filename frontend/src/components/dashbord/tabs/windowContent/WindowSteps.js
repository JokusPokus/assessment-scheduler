import React, {useState} from 'react';
import {Steps} from 'antd';
import './WindowSteps.css'
import CSVDashboard from "./CSV/CSVDashboard";
import SlotDashboard from "./slots/SlotDashboard";
import AvailDashboard from "./availabilities/AvailDashboard";

const {Step} = Steps;

const WindowSteps = ({window, setPhaseData}) => {
    const [current, setCurrent] = useState(0);
    const [uploadSuccess, setUploadSuccess] = useState(false);
    const [uploadErrors, setUploadErrors] = useState({});

    const steps = [
        {
            title: 'CSV',
            content: <CSVDashboard
                window={window}
                windowStep={current}
                setWindowStep={setCurrent}
                uploadSuccess={uploadSuccess}
                setUploadSuccess={setUploadSuccess}
                uploadErrors={uploadErrors}
                setUploadErrors={setUploadErrors}
            />,
        },
        {
            title: 'Slots',
            content: <SlotDashboard
                window={window}
                windowStep={current}
                setWindowStep={setCurrent}
                setPhaseData={setPhaseData}
            />,
        },
        {
            title: 'Availabilities',
            content: <AvailDashboard
                window={window}
            />
        },
        {
            title: 'Modules',
            content: 'Last-content',
        },
        {
            title: 'Rooms',
            content: 'Last-content',
        },
        {
            title: 'Schedule',
            content: 'Last-content',
        },
    ];

    const onChange = newStep => {
        setCurrent(newStep);
    };

    return (
        <div style={{marginTop: "20px"}}>
            <Steps current={current} onChange={onChange}>
                {steps.map(item => (
                    <Step key={item.title} title={item.title}/>
                ))}
            </Steps>
            <div className="steps-content">{steps[current].content}</div>
        </div>
    );
};

export default WindowSteps;
