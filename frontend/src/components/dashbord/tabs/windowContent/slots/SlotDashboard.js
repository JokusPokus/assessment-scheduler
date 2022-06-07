import React, {useEffect, useState} from 'react';
import {Statistic, Row, Col, TimePicker, message} from 'antd';
import BlockDateSelector from "./BlockDateSelector";
import {httpPostBlockSlots} from "../../../../../hooks/requests";
import {foldSlotData} from "../../../../../utils/dataTransform";
import getDaysArray from "../../../../../utils/datetime";

const format = 'HH:mm';
const _ = require('lodash');


const StatsRow = ({window, availableTimes, setAvailableTimes, startTimeData, setStartTimeData}) => {
    return (
        <>
            <Row
                justify="start"
                style={{marginTop: "80px", marginBottom: "50px"}}
            >
                <Col span={6}>
                    <Statistic
                        title="Start date"
                        value={window.start_date}
                    />
                </Col>
                <Col span={6}>
                    <Statistic
                        title="End date"
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
                    window={window}
                    availableTimes={availableTimes}
                    setAvailableTimes={setAvailableTimes}
                    startTimeData={startTimeData}
                    setStartTimeData={setStartTimeData}
                />
            </Row>
        </>
    );
};

const StartTimeSelector = ({window, availableTimes, setAvailableTimes, startTimeData, setStartTimeData}) => {
    const onChange = (time, timeString) => {
        let newAvailableTimes = [...availableTimes, timeString];
        newAvailableTimes.sort();
        setAvailableTimes(newAvailableTimes);

        const daysArray = getDaysArray(window.start_date, window.end_date);

        let timeData = startTimeData;
        for (const date of daysArray) {
            let newTimes;
            if (date in timeData) {
                newTimes = [...timeData[date], timeString];
            } else {
                newTimes = [timeString];
            }
            console.log(newTimes);
            newTimes.sort();
            timeData[date] = newTimes;
        }
        console.log(timeData);
        console.log("FFF", {...startTimeData, ...timeData});

        setStartTimeData({...startTimeData, ...timeData});
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
    const processStatus = {
        INITIAL: "initial",
        LOADING: "loading",
        SUCCESS: "success",
        FAILURE: "failure"
    };

    const [startTimeData, setStartTimeData] = useState({});
    const [availableTimes, setAvailableTimes] = useState([]);
    const [status, setStatus] = useState(processStatus.INITIAL);

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
        setStatus(processStatus.LOADING);

        const response = await httpPostBlockSlots(window.id, startTimeData)();
        await setPhaseData();
        if (response.status === 200) {
            message.success("You successfully saved the block slots.");
            setStatus(processStatus.SUCCESS);
        } else if (response.status === 400) {
            message.error("At least two slots were overlapping! Check again.");
            setStatus(processStatus.FAILURE);
        } else {
            message.error("Something went wrong...");
            setStatus(processStatus.FAILURE);
        }
    };

    return (
        <div className='fade-in'>
            <StatsRow
                window={window}
                availableTimes={availableTimes}
                setAvailableTimes={setAvailableTimes}
                startTimeData={startTimeData}
                setStartTimeData={setStartTimeData}
            />
            <BlockDateSelector
                window={window}
                startTimeData={startTimeData}
                setStartTimeData={setStartTimeData}
                availableTimes={availableTimes}
                saveTimes={saveTimes}
                status={status}
                windowStep={windowStep}
                setWindowStep={setWindowStep}
            />
        </div>
    );
};

export default SlotDashboard;
