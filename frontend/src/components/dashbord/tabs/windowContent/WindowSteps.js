import React, {useState} from 'react';
import {Steps} from 'antd';
import {UploadOutlined, DownloadOutlined, HistoryOutlined, TeamOutlined, HeartOutlined, BuildOutlined} from "@ant-design/icons";
import './WindowSteps.css'
import CSVDashboard from "./CSV/CSVDashboard";
import SlotDashboard from "./slots/SlotDashboard";
import AssessorDashboard from "./availabilities/AssessorDashboard";
import HelperDashboard from "./availabilities/HelperDashboard";
import ModuleDashboard from "./modules/ModuleDashboard";
import ScheduleDashboard from "./schedules/ScheduleDashboard";

const {Step} = Steps;


const WindowSteps = ({phase, window, setPhaseData}) => {
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
                setPhaseData={setPhaseData}
            />,
            icon: <UploadOutlined />
        },
        {
            title: 'Slots',
            content: <SlotDashboard
                window={window}
                windowStep={current}
                setWindowStep={setCurrent}
                setPhaseData={setPhaseData}
            />,
            icon: <HistoryOutlined />
        },
        {
            title: 'Assessors',
            content: <AssessorDashboard
                window={window}
                windowStep={current}
                setWindowStep={setCurrent}
                setPhaseData={setPhaseData}
            />,
            icon: <TeamOutlined />
        },
        {
            title: 'Helpers',
            content: <HelperDashboard
                window={window}
                windowStep={current}
                setWindowStep={setCurrent}
                setPhaseData={setPhaseData}
            />,
            icon: <HeartOutlined />
        },
        {
            title: 'Modules',
            content: <ModuleDashboard
                window={window}
                windowStep={current}
                setWindowStep={setCurrent}
            />,
            icon: <BuildOutlined />
        },
        {
            title: 'Schedule',
            content: <ScheduleDashboard
                phase={phase}
                window={window}
            />,
            icon: <DownloadOutlined />
        },
    ];

    const onChange = newStep => {
        setCurrent(newStep);
    };

    return (
        <div style={{marginTop: "20px"}}>
            <Steps current={current} onChange={onChange}>
                {steps.map(item => (
                    <Step
                        key={item.title}
                        title={item.title}
                        icon={item.icon}
                    />
                ))}
            </Steps>
            <div className="steps-content">{steps[current].content}</div>
        </div>
    );
};

export default WindowSteps;
