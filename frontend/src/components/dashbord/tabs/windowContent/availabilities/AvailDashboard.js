import React, {useEffect, useState} from 'react';
import getDaysArray from "../../../../../utils/datetime";
import {Table, Tag} from "antd";
import {httpGetAssessors} from "../../../../../hooks/requests";
import {foldSlotData} from "../../../../../utils/slots";

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
    };

    useEffect(() => {
        console.log("USED", availData);
        const nextAssessorAvails = {
            [assessor]: {
                ...(assessor in availData ? availData[assessor] : {}),
                [day]: selectedTags
            }
        };
        console.log({...availData, ...nextAssessorAvails});
        setAvailData({...availData, ...nextAssessorAvails});
    }, [selectedTags]);

    useEffect(() => {
        console.log(availData)
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
    console.log("YUPPU");
    const days = getDaysArray(window.start_date, window.end_date);
    const daysColumns = days.map(day => (
        {
            title: day,
            dataIndex: day,
            key: day,
        }
    ));

    const [assessors, setAssessors] = useState([]);
    const [assTableSource, setAssTableSource] = useState(null);
    const [availData, setAvailData] = useState({});

    const slotData = foldSlotData(window.block_slots);

    useEffect(() => {
        console.log(availData)
    }, [availData]);

    useEffect(async () => {
        const response = await httpGetAssessors(window.id)();
        let assess = await response.json();
        let assessEmails = assess.map(ass => ass.email);
        assessEmails.sort();
        setAssessors(assessEmails);
    }, []);

    useEffect(() => {
        const newAssTableSource = assessors && assessors.map(ass => {
            let dayElements = days.map(day => (
                {
                    [day]: <AvailChecks
                        key={day}
                        day={day}
                        assessor={ass}
                        availableTimes={slotData[day]}
                        availData={availData}
                        setAvailData={setAvailData}
                    />
                }
            ));
            return Object.assign(
                {
                    assessor: ass,
                    key: ass
                },
                ...dayElements
            );
        });
        setAssTableSource(newAssTableSource)
    }, [assessors]);

    return (
        <>
            <h1 style={{textAlign: 'left', marginTop: '80px', marginLeft: '10px'}}>
                Assessors
            </h1>
            <Table
                dataSource={assTableSource}
                columns={[...assessorColumn, ...daysColumns]}
                pagination={false}
            />
            <h1 style={{textAlign: 'left', marginTop: '80px', marginLeft: '10px'}}>
                Helpers
            </h1>
            {/*<Table
                dataSource={null}
                columns={[...helperColumn, ...daysColumns]}
                pagination={false}
            />*/}
        </>
    )
};

export default AvailDashboard;