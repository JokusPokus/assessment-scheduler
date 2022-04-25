import React, {useEffect, useState} from 'react';
import {Tag, Table, Button, Tooltip} from 'antd';
import {CheckOutlined, WarningOutlined} from "@ant-design/icons";
import getDaysArray from "../../../../../utils/datetime";

const {CheckableTag} = Tag;
const _ = require('lodash');

const columns = [
    {
        title: 'Day',
        dataIndex: 'day',
        key: 'day',
    },
    {
        title: 'Date',
        dataIndex: 'date',
        key: 'date',
    },
    {
        title: 'Block start times',
        dataIndex: 'startTimes',
        key: 'startTimes',
    }
];


const StartTimeChecks = ({day, startTimeData, setStartTimeData, availableTimes}) => {
    const [selectedTags, setSelectedTags] = useState([]);

    useEffect(() => {
        if (!_.isEmpty(startTimeData)) {
            setSelectedTags(day in startTimeData ? startTimeData[day] : []);
        }
    }, [startTimeData]);

    const handleChange = (tag, checked) => {
        const nextSelectedTags = checked ? [...selectedTags, tag] : selectedTags.filter(t => t !== tag);
        setSelectedTags(nextSelectedTags);
        setStartTimeData({...startTimeData, [day]: nextSelectedTags});
    };

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
    );
};

const BlockDateSelector = ({
                               window,
                               startTimeData,
                               setStartTimeData,
                               availableTimes,
                               saveTimes,
                               status,
                               windowStep,
                               setWindowStep
                           }) => {
    const daysArray = getDaysArray(window.start_date, window.end_date);
    const weekDays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    const [saveButtonDisabled, setSaveButtonDisabled] = useState(true);

    useEffect(() => {
        setSaveButtonDisabled(
            Object.values(startTimeData).every(x => x.length === 0)
        );
    }, [startTimeData]);

    const dataSource = daysArray.map((date, index) => {
        const weekDayIndex = new Date(date).getDay();
        return {
            key: index,
            day: weekDays[weekDayIndex],
            date: date,
            startTimes: <StartTimeChecks
                day={date}
                startTimeData={startTimeData}
                setStartTimeData={setStartTimeData}
                availableTimes={availableTimes}
            />
        }
    });

    return (
        <>
            <Table
                dataSource={dataSource}
                columns={columns}
                pagination={false}
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
                    onClick={saveTimes}
                    loading={status === "loading"}
                    disabled={saveButtonDisabled}
                    icon={status === "success"
                        ? <strong><CheckOutlined/> </strong>
                        : status === "failure"
                            ? <strong><WarningOutlined/> </strong>
                            : null
                    }
                >
                    <strong>Save times</strong>
                </Button>
            </Tooltip>

            {status === "success" && (
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
                    key="console"
                    onClick={() => setWindowStep(windowStep + 1)}
                >
                    <strong>Next step</strong>
                </Button>
            )}
        </>
    );
};

export default BlockDateSelector;
