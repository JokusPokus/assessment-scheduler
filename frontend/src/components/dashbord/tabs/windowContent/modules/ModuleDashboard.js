import React, {useEffect, useState} from 'react';
import {httpGetModules, httpPostModuleDurations} from "../../../../../hooks/requests";
import {InputNumber, message, Table, Tooltip} from "antd";
import {ClockCircleOutlined} from "@ant-design/icons";
import {SaveButton, NextStepButton} from "../Buttons";


const DurationInput = ({durationData, initialDuration, setDurationData, assessmentType, code}) => {
    const [duration, setDuration] = useState(initialDuration);

    const handleChange = (value) => {
        setDuration(value);

        const index = durationData.findIndex((obj => obj.code === code));
        durationData[index][`${assessmentType}_length`] = value;
        setDurationData(durationData);
    };

    return (
        <InputNumber
            min={20}
            max={30}
            step={10}
            value={duration}
            addonBefore={<ClockCircleOutlined/>}
            formatter={value => `${value} min`}
            parser={value => value.replace(' min', '')}
            style={{width: "50%"}}
            onStep={handleChange}
        />
    )
};


const ModuleDashboard = ({window, windowStep, setWindowStep}) => {
    const columns = [
        {
            title: 'Short Code',
            dataIndex: 'shortCode',
            key: 'shortCode',
        },
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
        },
        {
            title: 'Standard Assessment',
            dataIndex: 'standardAssessment',
            key: 'standardAssessment',
        },
        {
            title: 'Alternative Assessment',
            dataIndex: 'alternativeAssessment',
            key: 'alternativeAssessment',
        },
    ];

    const processStatus = {
        INITIAL: "initial",
        LOADING: "loading",
        SUCCESS: "success",
        FAILURE: "failure"
    };

    const [status, setStatus] = useState(processStatus.INITIAL);
    const [dataSource, setDataSource] = useState([]);
    const [durationData, setDurationData] = useState([]);

    const getModules = async () => {
        const response = await httpGetModules(window.id)();
        let moduleData = await response.json();
        setDurationData(moduleData);
    };

    useEffect(async () => {
        await getModules();
    }, []);

    useEffect(() => {
        const moduleTableSource = durationData.length > 0
            ? durationData.map(module => ({
                shortCode: module.code,
                name: module.name,
                standardAssessment: <DurationInput
                    key={`${module.code}_s`}
                    initialDuration={module.standard_length}
                    durationData={durationData}
                    setDurationData={setDurationData}
                    code={module.code}
                    assessmentType="standard"
                />,
                alternativeAssessment: <DurationInput
                    key={`${module.code}_a`}
                    initialDuration={module.alternative_length}
                    durationData={durationData}
                    setDurationData={setDurationData}
                    code={module.code}
                    assessmentType="alternative"
                />
            }))
            : [];
        setDataSource([...moduleTableSource]);
    }, [durationData]);

    const saveDurations = async () => {
        setStatus(processStatus.LOADING);
        setTimeout(async () => {
            const response = await httpPostModuleDurations(durationData)();
            if (response.status === 200) {
                message.success(`You successfully saved module durations.`);
                setStatus(processStatus.SUCCESS);
                await getModules();
            } else {
                message.error("Something went wrong...");
                setStatus(processStatus.FAILURE);
            }
        }, 1000);
    };

    return (
        <div className='fade-in'>
            <Table
                bordered
                dataSource={dataSource}
                columns={columns}
                tableLayout={"fixed"}
                pagination={false}
                style={{marginTop: "60px"}}
            />
            <SaveButton
                status={status}
                disabled={false}
                title="Save durations"
                onClick={saveDurations}
            />
            <NextStepButton
                windowStep={windowStep}
                setWindowStep={setWindowStep}
                status={status}
            />
        </div>
    )
};

export default ModuleDashboard;
