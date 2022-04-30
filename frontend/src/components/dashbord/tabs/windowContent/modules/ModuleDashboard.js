import React, {useEffect, useState} from 'react';
import {httpGetModules} from "../../../../../hooks/requests";
import {InputNumber, Table} from "antd";
import {ClockCircleOutlined} from "@ant-design/icons";


const DurationInput = () => {
    return (
        <InputNumber
            min={5}
            max={300}
            step={5}
            defaultValue={20}
            addonBefore={<ClockCircleOutlined />}
            style={{width: "50%"}}
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
    const [saveButtonDisabled, setSaveButtonDisabled] = useState(true);
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
        // Are all the durations empty?
        const mustDisable = durationData.map(obj => (!('duration' in obj)))
            .every(Boolean);
        setSaveButtonDisabled(mustDisable);
    }, [durationData]);

    useEffect(() => {
        const moduleTableSource = durationData.length > 0
            ? durationData.map(module => ({
                shortCode: module.code,
                name: module.name,
                standardAssessment: <DurationInput key={`${module.code}_s`}/>,
                alternativeAssessment: <DurationInput key={`${module.code}_a`}/>
            }))
            : [];
        setDataSource([...moduleTableSource]);
    }, [durationData]);

    return (
        <>
            <Table
                bordered
                dataSource={dataSource}
                columns={columns}
                tableLayout={"fixed"}
                pagination={false}
            />
        </>
    )
};

export default ModuleDashboard;
