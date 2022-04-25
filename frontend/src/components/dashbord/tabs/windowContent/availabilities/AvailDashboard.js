import React, {useEffect, useState} from 'react';
import getDaysArray from "../../../../../utils/datetime";
import {Button, message, Table, Tag, Tooltip} from "antd";
import {httpGetAssessors, httpPostAssessorAvails} from "../../../../../hooks/requests";
import {foldSlotData, foldAssessorData} from "../../../../../utils/dataTransform";
import {CheckOutlined, WarningOutlined} from "@ant-design/icons";

const _ = require('lodash');
const {CheckableTag} = Tag;

const assessorColumn = [
    {
        title: 'Assessor',
        dataIndex: 'assessor',
        key: 'assessor',
    },
];

const helperColumn = [
    {
        title: 'Helper',
        dataIndex: 'helper',
        key: 'helper',
    },
];


const AvailChecks = ({day, assessor, availableTimes, availData, setAvailData}) => {
    const [selectedTags, setSelectedTags] = useState([]);

    const handleChange = (tag, checked) => {
        const nextSelectedTags = checked ? [...selectedTags, tag] : selectedTags.filter(t => t !== tag);
        setSelectedTags(nextSelectedTags);

        const nextAssessorAvails = {
            [assessor]: {
                ...(assessor in availData ? availData[assessor] : {}),
                [day]: nextSelectedTags
            }
        };
        setAvailData({...availData, ...nextAssessorAvails});
    };

    useEffect(() => {
        if (assessor in availData && day in availData[assessor]) {
            setSelectedTags(availData[assessor][day])
        }
    }, [availData]);

    return (
        <>
            {availableTimes.map(tag => (
                <CheckableTag
                    key={tag}
                    checked={selectedTags.indexOf(tag) > -1}
                    onChange={checked => handleChange(tag, checked)}
                    style={{
                        padding: "8px",
                        fontSize: "1.1em"
                    }}
                >
                    {tag}
                </CheckableTag>
            ))}
        </>
    )
};


const AvailDashboard = ({window}) => {
    const days = getDaysArray(window.start_date, window.end_date);
    const daysColumns = days.map(day => (
        {
            title: day,
            dataIndex: day,
            key: day,
        }
    ));

    const processStatus = {
        INITIAL: "initial",
        LOADING: "loading",
        SUCCESS: "success",
        FAILURE: "failure"
    };

    const [assessors, setAssessors] = useState([]);
    const [availData, setAvailData] = useState({});
    const [status, setStatus] = useState(processStatus.INITIAL);
    const [saveButtonDisabled, setSaveButtonDisabled] = useState(true);

    const slotData = foldSlotData(window.block_slots);

    useEffect(async () => {
        const response = await httpGetAssessors(window.id)();
        let assess = await response.json();
        setAssessors(assess);
    }, []);

    useEffect(() => {
        setAvailData(foldAssessorData(assessors));
    }, [assessors]);

    useEffect(() => {
        const mustDisable = Object.values(availData).map(obj => (
                Object.values(obj).every(x => x.length === 0)
            )
        ).every(Boolean);
        setSaveButtonDisabled(mustDisable);
    }, [availData]);

    const saveAvails = async () => {
        setStatus(processStatus.LOADING);
        setTimeout(async () => {
            const response = await httpPostAssessorAvails(window.id, availData)();
            if (response.status === 200) {
                message.success("You successfully saved assessor availabilities.");
                setStatus(processStatus.SUCCESS);
            } else {
                message.error("Something went wrong...");
                setStatus(processStatus.FAILURE);
            }
        }, 1000);
    };

    const assTableSource = assessors.length > 0 && assessors.map(ass => {
        let dayElements = days.map(day => (
            {
                [day]: <AvailChecks
                    key={day}
                    day={day}
                    assessor={ass.email}
                    availableTimes={slotData[day]}
                    availData={availData}
                    setAvailData={setAvailData}
                />
            }
        ));
        return Object.assign(
            {
                assessor: ass.email,
                key: ass.email
            },
            ...dayElements
        );
    });

    return (
        <>
            <h1 style={{textAlign: 'left', marginTop: '80px', marginLeft: '10px'}}>
                Assessors
            </h1>
            <Table
                dataSource={assTableSource}
                columns={[...assessorColumn, ...daysColumns]}
                pagination={false}
                tableLayout={"fixed"}
            />
            <Tooltip title={saveButtonDisabled ? "Please add/select start times" : undefined}>
                <Button
                    type="primary"
                    shape="round"
                    size="large"
                    style={{
                        marginTop: "30px",
                        marginBottom: "30px",
                        marginRight: "20px",
                        float: "right"
                    }}
                    onClick={saveAvails}
                    loading={status === processStatus.LOADING}
                    disabled={saveButtonDisabled}
                    icon={status === processStatus.SUCCESS
                        ? <strong><CheckOutlined/> </strong>
                        : status === processStatus.FAILURE
                            ? <strong><WarningOutlined/> </strong>
                            : null
                    }
                >
                    <strong>Save availabilities</strong>
                </Button>
            </Tooltip>

            <h1 style={{textAlign: 'left', marginTop: '80px', marginLeft: '10px'}}>
                Helpers
            </h1>
            <Table
                dataSource={null}
                columns={[...helperColumn, ...daysColumns]}
                pagination={false}
            />
        </>
    )
};

export default AvailDashboard;