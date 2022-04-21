import React, {useState} from 'react';
import {Tag, Table, Button} from 'antd';
import {SaveOutlined} from "@ant-design/icons";
import getDaysArray from "../../../../utils/datetime";

const {CheckableTag} = Tag;

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


const StartTimeChecks = ({day, availableTimes}) => {
    const [selectedTags, setSelectedTags] = useState(availableTimes);

    const handleChange = (tag, checked) => {
        const nextSelectedTags = checked ? [...selectedTags, tag] : selectedTags.filter(t => t !== tag);
        setSelectedTags(nextSelectedTags);
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

const BlockDateSelector = ({window, availableTimes}) => {
    const daysArray = getDaysArray(window.start_date, window.end_date);
    const weekDays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    const [startTimeData, setStartTimeData] = useState({});

    const dataSource = daysArray.map((date, index) => {
        const weekDayIndex = new Date(date).getDay();
        return {
            key: index,
            day: weekDays[weekDayIndex],
            date: date,
            startTimes: <StartTimeChecks
                day={date}
                availableTimes={availableTimes}
            />
        }
    });

    const saveTimes = () => {
        console.log();
    };

    return (
        <>
            <Table
                dataSource={dataSource}
                columns={columns}
                pagination={false}
            />
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
            >
                <strong>Save times</strong>
            </Button>
        </>
    );
};

export default BlockDateSelector;
