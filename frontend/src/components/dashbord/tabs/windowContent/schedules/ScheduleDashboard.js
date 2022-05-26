import React from 'react';
import {Button, Col, Row, Statistic} from "antd";
import {httpTriggerScheduling} from "../../../../../hooks/requests";
import {DownloadOutlined} from "@ant-design/icons";
import './ScheduleDashboard.css'


const StatsRow = () => {
    return (
        <>
            <Row
                justify="start"
                style={{marginTop: "80px", marginBottom: "20px"}}
            >
                <Col span={6}>
                    <Statistic
                        className={'statsCard'}
                        title="Start date"
                        value={'12-12-2022'}
                    />
                </Col>
                <Col span={6}>
                    <Statistic
                        className={'statsCard'}
                        title="End date"
                        value={'24-12-2022'}
                    />
                </Col>
                <Col span={6}>
                    <Statistic
                        className={'statsCard'}
                        title="Block length"
                        value={180}
                        suffix="min"
                    />
                </Col>
                <Col span={6}>
                    <Statistic
                        className={'statsCard'}
                        title="Exams to schedule"
                        value={19}
                        valueStyle={{ color: '#3f8600' }}
                    />
                </Col>
            </Row>
            <Row
                justify="start"
                style={{marginTop: "50px", marginBottom: "50px"}}
            >
                <Col span={6}>
                    <Statistic
                        className={'statsCard'}
                        title="CSV sheet"
                        value={`OK`}
                        valueStyle={{ color: '#3f8600' }}
                    />
                </Col>
                <Col span={6}>
                    <Statistic
                        className={'statsCard'}
                        title="Assessor availabilities"
                        value={5}
                        suffix={`/ 6`}
                        valueStyle={{ color: '#cf1322' }}
                    />
                </Col>
                <Col span={6}>
                    <Statistic
                        className={'statsCard'}
                        title="Helpers"
                        value={4}
                        valueStyle={{ color: '#3f8600' }}
                    />
                </Col>
                <Col span={6}>
                    <Statistic
                        className={'statsCard'}
                        title="Penalty"
                        value={'-'}
                        valueStyle={{ color: '#3f8600' }}
                    />
                </Col>
            </Row>
        </>
    );
};


const ScheduleDashboard = ({window}) => {
    const triggerScheduling = async () => {
        await httpTriggerScheduling(window.id)();
    };

    return (
        <>
            <StatsRow/>
            <Button
                className={'fade-in'}
                type="primary"
                shape="round"
                size="large"
                style={{
                    marginTop: "30px",
                    marginBottom: "30px",
                    marginRight: "30px"
                }}
                onClick={triggerScheduling}
            >
                <strong>Trigger scheduling process</strong>
            </Button>
            <Button
                className={'fade-in'}
                type="primary"
                shape="round"
                size="large"
                disabled={true}
                style={{
                    marginTop: "30px",
                    marginBottom: "30px",

                }}
                icon={<strong><DownloadOutlined /> </strong>}
            >
                <strong>Download CSV</strong>
            </Button>
        </>
    )
};

export default ScheduleDashboard;
