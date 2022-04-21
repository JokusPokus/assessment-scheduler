import React from 'react';
import {Statistic, Row, Col, TimePicker} from 'antd';
import {LikeOutlined, CalendarOutlined} from '@ant-design/icons';
import getDaysArray from "../../../../utils/datetime";
import moment from 'moment';
import BlockDateSelector from "./BlockDateSelector";

const format = 'HH:mm';


const StatsRow = ({window}) => {
    return (
        <Row
            justify="start"
            style={{marginTop: "50px"}}
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
        </Row>
    );
};

const StartTimeSelector = () => {
    return (
        <TimePicker
            bordered={false}
            minuteStep={15}
            showNow={false}
            defaultValue={moment('10:00', format)}
            format={format}
        />
    );
};

const BlockDashboard = ({window}) => {

    return (
        <>
            <StatsRow window={window}/>
            <StartTimeSelector/>
            <BlockDateSelector window={window}/>
        </>
    );
};

export default BlockDashboard;
