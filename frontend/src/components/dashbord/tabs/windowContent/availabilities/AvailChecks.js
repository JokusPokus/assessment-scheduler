import React, {useEffect, useState} from "react";
import {Tag} from "antd";

const _ = require('lodash');
const {CheckableTag} = Tag;

const AvailChecks = ({day, staff, availableTimes, availData, setAvailData}) => {
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
        console.log('new ad:', {...availData, ...nextAssessorAvails})
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

export default AvailChecks;
