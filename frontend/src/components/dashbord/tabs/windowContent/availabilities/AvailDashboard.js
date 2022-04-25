import React, {useEffect, useState} from 'react';
import getDaysArray from "../../../../../utils/datetime";
import {Button, message, Table, Tag, Tooltip} from "antd";
import {httpGetAssessors, httpPostAssessorAvails} from "../../../../../hooks/requests";
import {foldSlotData, foldAssessorData} from "../../../../../utils/dataTransform";
import {CheckOutlined, WarningOutlined} from "@ant-design/icons";
import HelpersTable from "./HelpersTable";
import AvailChecks from "./AvailChecks";

const _ = require('lodash');

const assessorColumn = [
    {
        title: 'Assessor',
        dataIndex: 'assessor',
        key: 'assessor',
        width: '25%',
    },
];


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

    const getAssessors = async () => {
        const response = await httpGetAssessors(window.id)();
        let assess = await response.json();
        assess = assess.map(ass => (
            {
                ...ass,
                available_blocks: ass.available_blocks.filter(
                    block => block.window === window.id
                )
            }
        ));
        setAssessors(assess);
    };

    useEffect(async () => {
        await getAssessors();
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
                await getAssessors();
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
                bordered
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
            <HelpersTable window={window}/>
        </>
    )
};

export default AvailDashboard;