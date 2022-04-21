import React, {useState} from 'react';
import {Statistic, Row, Col, TimePicker} from 'antd';
import {LikeOutlined, CalendarOutlined} from '@ant-design/icons';
import getDaysArray from "../../../../utils/datetime";
import moment from 'moment';
import BlockDateSelector from "./BlockDateSelector";

const format = 'HH:mm';


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
        console.log(newAvailableTimes);
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
    const [availableTimes, setAvailableTimes] = useState(['10:00', '14:00']);

    return (
        <>
            <StatsRow
                window={window}
                availableTimes={availableTimes}
                setAvailableTimes={setAvailableTimes}
            />
            <BlockDateSelector window={window} availableTimes={availableTimes}/>
        </>
    );
};

export default BlockDashboard;
