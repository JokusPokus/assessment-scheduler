import React, {useEffect, useState} from 'react';
import {Button, Col, Row, Statistic, Result} from "antd";
import {
    httpTriggerScheduling,
    httpGetSchedulingStatus,
    httpGetScheduleEvaluation, httpGetCSV,
} from "../../../../../hooks/requests";
import {DownloadOutlined, RocketOutlined} from "@ant-design/icons";
import './ScheduleDashboard.css'


const StatsRow = ({window, penalty}) => {
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
                        className={`statsCard ${penalty === null ? 'unblocked' : 'highlighted'}`}
                        title="Penalty"
                        value={penalty === null ? '-' : penalty}
                    />
                </Col>
            </Row>
        </>
    );
};


const ScheduleDashboard = ({window: schedWindow}) => {
        const Status = {
            IDLE: 'idle',
            ONGOING: 'ongoing',
            DONE: 'done'
        };

        const [schedulingStatus, setSchedulingStatus] = useState(Status.IDLE);
        const [penalty, setPenalty] = useState(null);

        useEffect(async () => {
            const response = await httpGetSchedulingStatus(schedWindow.id)();
            const payload = await response.json();
            setSchedulingStatus(payload.scheduling_status);
        }, []);

        useEffect(async () => {
            if (schedulingStatus === Status.DONE) {
                const response = await httpGetScheduleEvaluation(schedWindow.id)();
                const payload = await response.json();
                setPenalty(payload.penalty);
            }
        }, [schedulingStatus]);

        const getScheduleStatus = async () => {
            setTimeout(async () => {
                const response = await httpGetSchedulingStatus(schedWindow.id)();
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
            schedWindow.total_assessors > 0,
            schedWindow.available_assessors === schedWindow.total_assessors,
            schedWindow.csv_uploaded
        ];

        const goodToGo = scheduleConditions.every(Boolean);

        useEffect(async () => {
            if (schedulingStatus === Status.ONGOING) {
                await httpTriggerScheduling(schedWindow.id)();
            }
        }, [schedulingStatus]);

        const downloadCSV = async () => {
            const response = await httpGetCSV(schedWindow.id)();
            const blob = await response.blob();
            let url = window.URL.createObjectURL(blob);
            let a = document.createElement('a');
            a.href = url;
            a.download = 'schedule.csv';
            a.click();
        };

        return (
            <>
                {schedulingStatus === Status.DONE &&
                <Result
                    className={'fade-in'}
                    icon={<RocketOutlined/>}
                    title="Looks like we found a solution!"
                    style={{paddingBottom: '0'}}
                    extra={<Button
                        className={'fade-in'}
                        type="primary"
                        shape="round"
                        size="large"
                        style={{
                            marginTop: "30px",
                        }}
                        icon={<strong><DownloadOutlined/> </strong>}
                        onClick={() => downloadCSV()}
                    >
                        <strong>Download CSV</strong>
                    </Button>}
                />
                }
                <StatsRow window={schedWindow} penalty={penalty}/>
                <Button
                    id={goodToGo ? '' : 'schedulingBlocked'}
                    className={"fade-in"}
                    type="primary"
                    shape="round"
                    size="large"
                    style={{
                        marginTop: "30px",
                        marginBottom: "30px"
                    }}
                    disabled={!goodToGo}
                    loading={schedulingStatus === Status.ONGOING}
                    onClick={() => setSchedulingStatus(Status.ONGOING)}
                >
                    <strong>Trigger scheduling process</strong>
                </Button>
            </>
        )
    }
;

export default ScheduleDashboard;
