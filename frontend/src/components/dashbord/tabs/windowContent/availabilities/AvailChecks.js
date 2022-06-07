import React, {useEffect, useState} from "react";
import {Button, Tag} from "antd";

const _ = require('lodash');
const {CheckableTag} = Tag;


export const SelectAll = ({staff, availData, setAvailData, slotData}) => {
    const selectAll = () => {
        const staffAvails = {[staff]: slotData};
        setAvailData({...availData, ...staffAvails});
    };

    return (
        <Button
            shape={'round'}
            onClick={selectAll}
        >
            Select all
        </Button>
    )
};


export const AvailChecks = ({day, staff, availableTimes, availData, setAvailData}) => {
    const [selectedTags, setSelectedTags] = useState([]);

    const handleChange = (tag, checked) => {
        const nextSelectedTags = checked ? [...selectedTags, tag] : selectedTags.filter(t => t !== tag);
        setSelectedTags(nextSelectedTags);

        const nextAssessorAvails = {
            [staff]: {
                ...(staff in availData ? availData[staff] : {}),
                [day]: nextSelectedTags
            }
        };
        setAvailData({...availData, ...nextAssessorAvails});
    };

    useEffect(() => {
        if (staff in availData && day in availData[staff]) {
            setSelectedTags(availData[staff][day])
        }
    }, [availData]);

    return (
        <>
            {availableTimes && availableTimes.map(tag => (
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
