import {Button, Select, Tooltip } from "antd";
import {PlusOutlined} from "@ant-design/icons";
import React, {useEffect, useState} from "react";
import usePhases from "../../hooks/callbacks";
import {httpPostPhase} from "../../hooks/requests";
import PhaseCreateForm from "./PhaseCreateForm";

const PhaseSelector = ({currentPhase, setCurrentPhase}) => {
    const phases = usePhases();
    const [years, setYears] = useState(undefined);
    const [semesterChoices, setSemesterChoices] = useState([]);

    useEffect(() => {
        if (!currentPhase && phases.length !== 0) {
            const years = Object.keys(phases);
            setYears(years);
            setCurrentPhase({
                year: years[0],
                semester: phases[years[0]][0],
                category: "main"
            });
            setSemesterChoices(phases[years[0]]);
        }
    }, [phases]);

    const handleYearChange = value => {
        setSemesterChoices(phases[value]);
        setCurrentPhase({
            ...currentPhase,
            year: value,
            semester: semesterChoices[0]
        })
    };

    const onPhaseChange = value => {
        setCurrentPhase({...currentPhase, semester: value})
    };

    const [visible, setVisible] = useState(false);

    const onCreate = (values) => {
        httpPostPhase({...values, category: "main"})();
        setVisible(false);
    };

    return (
        <div className="phase-selection-group">
            <Button className='phases-button' type={'link'}>
                Assessment Phase:
            </Button>
            {years &&
            <>
                <Select
                    defaultValue={years[0]}
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