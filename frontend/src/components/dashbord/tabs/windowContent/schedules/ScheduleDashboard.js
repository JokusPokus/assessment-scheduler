import React from 'react';
import {Button, Col, Row, Statistic} from "antd";
import {httpTriggerScheduling} from "../../../../../hooks/requests";
import {DownloadOutlined} from "@ant-design/icons";
import './ScheduleDashboard.css'


const StatsRow = ({window}) => {
    const assessorsOk = window.total_assessors > 0
        && window.available_assessors === window.total_assessors;

    return (
        <>
            <Row
                justify="start"
                style={{marginTop: "80px", marginBottom: "20px"}}
            >
                <Col span={6}>
                    <Statistic
                        className={'statsCard unblocked'}
                        title="Start date"
                        value={window.start_date}
                    />
                </Col>
                <Col span={6}>
                    <Statistic
                        className={'statsCard unblocked'}
                        title="End date"
                        value={window.end_date}
                    />
                </Col>
                <Col span={6}>
                    <Statistic
                        className={'statsCard unblocked'}
                        title="Block length"
                        value={window.block_length}
                        suffix="min"
                    />
                </Col>
                <Col span={6}>
                    <Statistic
                        className={'statsCard unblocked'}
                        title="Exams to schedule"
                        value={window.total_exams}
                    />
                </Col>
            </Row>
            <Row
                justify="start"
                style={{marginTop: "50px", marginBottom: "50px"}}
            >
                <Col span={6}>
                    <Statistic
                        className={`statsCard ${window.csv_uploaded ? 'unblocked' : 'blocked'}`}
                        title="CSV sheet"
                        value={window.csv_uploaded ? "OK" : "missing"}
                        valueStyle={{
                            color: window.csv_uploaded ? '#3f8600' : '#cf1322'
                        }}
                    />
                </Col>
                <Col span={6}>
                    <Statistic
                        className={`statsCard ${assessorsOk ? 'unblocked' : 'blocked'}`}
                        title="Assessor availabilities"
                        value={window.available_assessors}
                        suffix={`/ ${window.total_assessors}`}
                        valueStyle={{
                            color: assessorsOk
                                ? '#3f8600'
                                : '#cf1322'
                        }}
                    />
                </Col>
                <Col span={6}>
                    <Statistic
                        className={'statsCard unblocked'}
                        title="Helpers"
                        value={window.total_helpers}
                    />
                </Col>
                <Col span={6}>
                    <Statistic
                        className={'statsCard unblocked'}
                        title="Penalty"
                        value={'-'}
                    />
                </Col>
            </Row>
        </>
    );
};


const ScheduleDashboard = ({window}) => {

    const scheduleConditions = [
        window.total_assessors > 0,
        window.available_assessors === window.total_assessors,
        window.csv_uploaded
    ];

    const goodToGo = scheduleConditions.every(Boolean);

    const triggerScheduling = async () => {
        await httpTriggerScheduling(window.id)();
    };

    return (
        <>
            <StatsRow window={window} />
            <Button
                id={goodToGo ? '' : 'schedulingBlocked'}
                className={"fade-in"}
                type="primary"
                shape="round"
                size="large"
                style={{
                    marginTop: "30px",
                    marginBottom: "30px",
                    marginRight: "30px"
                }}
                disabled={!goodToGo}
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
