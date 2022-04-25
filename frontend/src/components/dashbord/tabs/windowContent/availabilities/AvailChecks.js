import React, {useEffect, useState} from "react";
import {Tag} from "antd";

const _ = require('lodash');
const {CheckableTag} = Tag;

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
