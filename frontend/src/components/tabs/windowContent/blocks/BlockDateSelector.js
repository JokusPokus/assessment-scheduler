import React, {useState} from 'react';
import {Tag, Table} from 'antd';
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


const StartTimeChecks = ({day}) => {
    const [selectedTags, setSelectedTags] = useState(['10:00', '14:00']);
    const tagsData = ['10:00', '14:00'];

    const handleChange = (tag, checked) => {
        const nextSelectedTags = checked ? [...selectedTags, tag] : selectedTags.filter(t => t !== tag);
        setSelectedTags(nextSelectedTags);
    };

    return (
        <>
            {tagsData.map(tag => (
                <CheckableTag
                    key={tag}
                    checked={selectedTags.indexOf(tag) > -1}
                    onChange={checked => handleChange(tag, checked)}
                >
                    {tag}
                </CheckableTag>
            ))}
        </>
    );
};

const BlockDateSelector = ({window}) => {
    let daysArray = getDaysArray(window.start_date, window.end_date);
    const weekDays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    const dataSource = daysArray.map((date, index) => {
        const weekDayIndex = new Date(date).getDay();
        return {
            key: index,
            day: weekDays[weekDayIndex],
            date: date,
            startTimes: <StartTimeChecks day={date}/>
        }
    });

    return (
        <Table
            dataSource={dataSource}
            columns={columns}
            pagination={false}
        />
    );
};

export default BlockDateSelector;
