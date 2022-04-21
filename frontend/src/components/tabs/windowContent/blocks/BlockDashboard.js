import React, {useEffect, useState} from 'react';
import {Statistic, Row, Col, TimePicker} from 'antd';
import {LikeOutlined, CalendarOutlined} from '@ant-design/icons';
import getDaysArray from "../../../../utils/datetime";
import moment from 'moment';
import BlockDateSelector from "./BlockDateSelector";
import {httpGetPhases} from "../../../../hooks/requests";

const format = 'HH:mm';
const _ = require('lodash');


const StatsRow = ({window, availableTimes, setAvailableTimes}) => {
    return (
        <>
            <Row
                justify="start"
                style={{marginTop: "50px", marginBottom: "50px"}}
            >
                <Col span={6}>
                    <Statistic
                        title="Start Date"
                        value={window.start_date}
                    />
                </Col>
                <Col span={6}>
                    <Statistic
                        title="End Date"
                        value={window.end_date}
                    />
                </Col>
                <Col span={6}>
                    <Statistic
                        title="Block length"
                        value={window.block_length}
                        suffix="min"
                    />
                </Col>
                <StartTimeSelector
                    availableTimes={availableTimes}
                    setAvailableTimes={setAvailableTimes}
                />
            </Row>
        </>
    );
};

const StartTimeSelector = ({availableTimes, setAvailableTimes}) => {
    const onChange = (time, timeString) => {
        let newAvailableTimes = [...availableTimes, timeString];
        newAvailableTimes.sort();
        setAvailableTimes(newAvailableTimes)
    };

    return (
        <Col span={6}>
            <p style={{color: "rgba(0, 0, 0, 0.45)", marginBottom: "8px"}}>
                Add start time
            </p>
            <TimePicker
                minuteStep={15}
                showNow={false}
                defaultValue={moment('10:00', format)}
                format={format}
                style={{fontSize: "24px"}}
                onChange={onChange}
            />
        </Col>
    );
};

const BlockDashboard = ({window}) => {
    const [startTimeData, setStartTimeData] = useState({});
    const [availableTimes, setAvailableTimes] = useState([]);

    useEffect(() => {
        if (!_.isEmpty(window)) {
            setStartTimeData(
                window.block_slots.reduce((r, a) => {
                    r[a.date] = r[a.date] || [];
                    r[a.date].push(a.time);
                    return r;
                }, Object.create(null))
            );

        }
    }, []);

    useEffect(() => {
        if (!_.isEmpty(startTimeData)) {
            setAvailableTimes([...new Set(
                startTimeData.reduce((r, a) => {
                    r.push(a.time);
                    return r;
                }, [])
            )]);
        }
    }, [startTimeData]);

    return (
        <>
            <StatsRow
                window={window}
                availableTimes={availableTimes}
                setAvailableTimes={setAvailableTimes}
            />
            <BlockDateSelector
                window={window}
                startTimeData={startTimeData}
                setStartTimeData={setStartTimeData}
                availableTimes={availableTimes}
            />
        </>
    );
};

export default BlockDashboard;
