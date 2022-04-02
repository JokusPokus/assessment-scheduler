import {Button, Select, Tooltip } from "antd";
import {PlusOutlined} from "@ant-design/icons";
import React, {useEffect, useState} from "react";
import getFormattedPhases from "../../hooks/callbacks";
import {httpPostPhase} from "../../hooks/requests";
import PhaseCreateForm from "./PhaseCreateForm";

const PhaseSelector = ({currentPhase, setCurrentPhase}) => {
    const [phases, setPhases] = useState([]);
    const [newPhaseCounter, setNewPhaseCounter] = useState([]);
    const [years, setYears] = useState([]);
    const [semesterChoices, setSemesterChoices] = useState([]);

    useEffect(() => {
        getFormattedPhases()
            .then(data => {setPhases(data)});
    }, [newPhaseCounter]);

    useEffect(() => {
        const years = Object.keys(phases);
        years.reverse();
        setYears(years);
        if (years.length !== 0) {
            const currentSemesterChoices = phases[years[0]];
            setSemesterChoices(currentSemesterChoices);
            setCurrentPhase({
                year: years[0],
                semester: currentSemesterChoices.slice(-1)[0],
                category: "main"
            });
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
                        <Select.Option key={semester}>{semester}</Select.Option>
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