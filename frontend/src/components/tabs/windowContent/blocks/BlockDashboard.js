import React from 'react';
import {Statistic, Row, Col} from 'antd';
import {LikeOutlined, CalendarOutlined} from '@ant-design/icons';


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


const BlockDashboard = ({window}) => {
    return (
        <StatsRow window={window}/>
    );
};

export default BlockDashboard;
