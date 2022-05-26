import React, {useEffect, useState} from 'react';
import {Button, Col, Row, Statistic} from "antd";
import {httpTriggerScheduling, httpGetSchedulingStatus} from "../../../../../hooks/requests";
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
    const Status = {
        IDLE: 'idle',
        ONGOING: 'ongoing',
        DONE: 'done'
    };

    const [schedulingStatus, setSchedulingStatus] = useState(Status.IDLE);

    useEffect(async () => {
        const response = await httpGetSchedulingStatus(window.id)();
        const payload = await response.json();
        setSchedulingStatus(payload.scheduling_status);
        console.log('SET')
    }, []);

    const getScheduleStatus = async () => {
        setTimeout(async () => {
            const response = await httpGetSchedulingStatus(window.id)();
            const payload = await response.json();

            if (payload.scheduling_status !== Status.ONGOING) {
                setSchedulingStatus(payload.scheduling_status);
            } else {
                await getScheduleStatus();
            }
        }, 10000);
    };

    useEffect(async () => {
        if (schedulingStatus === Status.ONGOING) {
            await getScheduleStatus();
        }
    }, [schedulingStatus]);

    const scheduleConditions = [
        window.total_assessors > 0,
        window.available_assessors === window.total_assessors,
        window.csv_uploaded
    ];

    const goodToGo = scheduleConditions.every(Boolean);

    useEffect(async () => {
        if (schedulingStatus === Status.ONGOING) {
            await httpTriggerScheduling(window.id)();
        }
    }, [schedulingStatus]);

    return (
        <>
            <div>{schedulingStatus}</div>
            <StatsRow window={window}/>
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
                onClick={() => setSchedulingStatus(Status.ONGOING)}
            >
                <strong>Trigger scheduling process</strong>
            </Button>
            <Button
                className={'fade-in'}
                type="primary"
                shape="round"
                size="large"
                disabled={schedulingStatus !== Status.DONE}
                style={{
                    marginTop: "30px",
                    marginBottom: "30px"
                }}
                icon={<strong><DownloadOutlined/> </strong>}
            >
                <strong>Download CSV</strong>
            </Button>
        </>
    )
};

export default ScheduleDashboard;
