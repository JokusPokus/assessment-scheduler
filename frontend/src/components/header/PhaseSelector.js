import {Button, Select, Tooltip} from "antd";
import {PlusOutlined} from "@ant-design/icons";
import React, {useEffect, useState} from "react";
import getFormattedPhases from "../../hooks/callbacks";
import {httpPostPhase, httpGetPhase} from "../../hooks/requests";
import PhaseCreateForm from "./PhaseCreateForm";

const semesterDisplay = {
    spring: "Spring Semester",
    fall: "Fall Semester"
};

const PhaseSelector = ({currentPhase, setCurrentPhase}) => {
    const [phases, setPhases] = useState([]);
    const [newPhaseCounter, setNewPhaseCounter] = useState([]);
    const [years, setYears] = useState([]);
    const [semesterChoices, setSemesterChoices] = useState([]);

    useEffect(() => {
        getFormattedPhases()
            .then(data => {
                setPhases(data)
            });
    }, [newPhaseCounter]);

    const setPhaseData = async (year, semester) => {
        const newPhase = await httpGetPhase({year: year, semester: semester})();
        setCurrentPhase(newPhase);
        console.log(newPhase);
    };

    useEffect(async () => {
        const years = Object.keys(phases);
        years.reverse();

        if (years.length !== 0) {
            setYears(years);

            const latestYear = years[0];
            const currentSemesterChoices = phases[latestYear];
            setSemesterChoices(currentSemesterChoices);
            await setPhaseData(latestYear, currentSemesterChoices.slice(-1)[0])
        }
    }, [phases]);

    const handleYearChange = value => {
        const currentSemesterChoices = phases[value];
        setSemesterChoices(currentSemesterChoices);
        setCurrentPhase({
            ...currentPhase,
            year: value,
            semester: currentSemesterChoices[0]
        })
    };

    const onPhaseChange = value => {
        setCurrentPhase({...currentPhase, semester: value})
    };

    const [visible, setVisible] = useState(false);

    const onCreate = async (values) => {
        await httpPostPhase({...values, category: "main"})();
        setNewPhaseCounter(newPhaseCounter + 1);
        setVisible(false);
    };

    return (
        <div className="phase-selection-group">
            <Button className='phases-button' type={'link'}>
                Assessment Phase:
            </Button>
            {years.length !== 0 &&
            <>
                <Select
                    value={currentPhase.year}
                    style={{width: 120, marginLeft: "30px"}}
                    onChange={handleYearChange}
                    bordered={false}
                >
                    {years.map(year => (
                        <Select.Option key={year}>{year}</Select.Option>
                    ))}
                </Select>
                <Select
                    style={{width: 240, marginLeft: "30px"}}
                    value={currentPhase.semester}
                    onChange={onPhaseChange}
                    bordered={false}
                >
                    {semesterChoices.map(semester => (
                        <Select.Option key={semester}>{semesterDisplay[semester]}</Select.Option>
                    ))}
                </Select>
                <Tooltip title="Add new phase">
                    <Button
                        shape="circle"
                        style={{marginLeft: "20px"}}
                        icon={<PlusOutlined/>}
                        onClick={() => {
                            setVisible(true);
                        }}
                    />
                </Tooltip>
                <PhaseCreateForm
                    visible={visible}
                    onCreate={onCreate}
                    onCancel={() => {
                        setVisible(false);
                    }}
                />
            </>
            }
        </div>
    )
};

export default PhaseSelector;