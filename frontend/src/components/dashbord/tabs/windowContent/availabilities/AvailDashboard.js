import React, {useEffect, useState} from 'react';
import getDaysArray from "../../../../../utils/datetime";
import {Table} from "antd";
import {httpGetAssessors} from "../../../../../hooks/requests";

const _ = require('lodash');

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


const AvailDashboard = ({window}) => {
    const days = getDaysArray(window.start_date, window.end_date);
    const daysColumns = days.map(day => (
        {
            title: day,
            dataIndex: day,
            key: day,
        }
    ));

    const [assessors, setAssessors] = useState([]);

    useEffect(async() => {
        const response = await httpGetAssessors(window.id)();
        let assess = await response.json();
        assess.sort();
        setAssessors((assess).map(ass => ass.email))
    }, []);

    return (
        <>
            <h1 style={{textAlign: 'left', marginTop: '80px', marginLeft: '10px'}}>
                Assessors
            </h1>
            <Table
                dataSource={assessors && assessors.map(ass => ({assessor: ass}))}
                columns={[...assessorColumn, ...daysColumns]}
                pagination={false}
            />
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