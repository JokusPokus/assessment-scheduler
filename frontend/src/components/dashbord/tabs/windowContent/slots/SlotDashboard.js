import React, {useEffect, useState} from 'react';
import {Statistic, Row, Col, TimePicker, message} from 'antd';
import BlockDateSelector from "./BlockDateSelector";
import {httpPostBlockSlots} from "../../../../../hooks/requests";
import {foldSlotData} from "../../../../../utils/slots";

const format = 'HH:mm';
const _ = require('lodash');


const StatsRow = ({window, availableTimes, setAvailableTimes}) => {
    return (
        <>
            <Row
                justify="start"
                style={{marginTop: "80px", marginBottom: "50px"}}
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
                format={format}
                style={{fontSize: "24px"}}
                onChange={onChange}
            />
        </Col>
    );
};

const SlotDashboard = ({window, windowStep, setWindowStep, setPhaseData}) => {
    const [startTimeData, setStartTimeData] = useState({});
    const [availableTimes, setAvailableTimes] = useState([]);
    const [isSuccess, setIsSuccess] = useState(false);
    const [isFailure, setIsFailure] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!_.isEmpty(window)) {
            setStartTimeData(foldSlotData(window.block_slots));
        }
    }, []);

    useEffect(() => {
        if (!_.isEmpty(startTimeData)) {
            let consideredTimes = Object.keys(startTimeData).reduce((r, a) => {
                r.push(...startTimeData[a]);
                return r;
            }, []);
            consideredTimes.push(...availableTimes);
            consideredTimes.sort();
            setAvailableTimes([...new Set(consideredTimes)]);
        }
    }, [startTimeData]);

    const saveTimes = async () => {
        setLoading(true);
        setTimeout(async () => {
            const response = await httpPostBlockSlots(window.id, startTimeData)();
            await setPhaseData();
            if (response.status === 200) {
                message.success("You successfully saved the block slots.");
                setLoading(false);
                setIsSuccess(true);
                setIsFailure(false);
            } else if (response.status === 400) {
                message.error("At least two slots were overlapping! Check again.");
                setLoading(false);
                setIsSuccess(false);
                setIsFailure(true);
            } else {
                message.error("Something went wrong...");
                setLoading(false);
                setIsSuccess(false);
                setIsFailure(true);
            }
        }, 1000);
    };

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
                saveTimes={saveTimes}
                loading={loading}
                isSuccess={isSuccess}
                isFailure={isFailure}
                windowStep={windowStep}
                setWindowStep={setWindowStep}
            />
        </>
    );
};

export default SlotDashboard;
