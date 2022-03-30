import { Button, Select, Layout, Tooltip } from "antd";
import { HomeOutlined, LogoutOutlined } from '@ant-design/icons';
import { Link } from "react-router-dom";
import React from "react";


const PortalHeader = ({ phase, setPhase, phases, setPhases, phaseData, userInfo}) => {
    const years = Object.keys(phaseData);

    const handleYearChange = value => {
        setPhases(phaseData[value]);
        setPhase(phaseData[value][0]);
    };

    const onPhaseChange = value => {
        setPhase(value);
    };

    return (
        <Layout.Header className="navbar-layout-background" >
            <div className='navbar-content'>
                <div className="phase-selection-group">
                    <Button className='phases-button' type={'link'}>
                        Assessment Phase:
                    </Button>
                    <Select
                        defaultValue={years[0]}
                        style={{ width: 120, marginLeft: "30px" }}
                        onChange={handleYearChange}
                        bordered={false}
                    >
                        {years.map(year => (
                            <Select.Option key={year}>{year}</Select.Option>
                        ))}
                    </Select>
                    <Select
                        style={{ width: 240, marginLeft: "30px" }}
                        value={phase}
                        onChange={onPhaseChange}
                        bordered={false}
                    >
                        {phases.map(assessPhase => (
                            <Select.Option key={assessPhase}>{assessPhase}</Select.Option>
                        ))}
                    </Select>
                </div>
                {userInfo &&
                    <div>
                        <HomeOutlined />
                        <Button className='org-button' type={'link'} style={{ color: 'black'}}>
                            {userInfo['organization']['name']}
                        </Button>
                    </div>
                }
            </div>
        </Layout.Header>
    )
};

export default PortalHeader;