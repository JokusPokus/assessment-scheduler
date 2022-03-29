import React from 'react';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Button, Layout, Select } from 'antd';
import './Portal.css'
import SideBar from '../../components/sideBar/SideBar';

const { Header, Content, Footer } = Layout;
const { Option } = Select;

const UserPortal = ({ requestUrl, refreshRequestBody }) => {
    const phaseData = {
        2022: ["Spring Semester", "Fall Semester"],
        2021: ["Fall Semester"],
    };
    const years = Object.keys(phaseData);

    const [activeTab, setActiveTab] = useState('main');

    const changeActiveTab = (tabName) => {
        return (event) => {
            setActiveTab(tabName);
        }
    };

    const [activeTabComponent, setActiveTabComponent] = useState(
        <h1>Welcome, user!</h1>
    );

    const [phases, setPhases] = useState(phaseData[years[0]]);
    const [phase, setPhase] = useState(phaseData[years[0]][0]);

    const handleYearChange = value => {
        setPhases(phaseData[value]);
        setPhase(phaseData[value][0]);
    };

    const onPhaseChange = value => {
        setPhase(value);
    };

    useEffect(() => {
        const tabs = {
            MAIN: "main",
        };

        switch (activeTab) {
            case tabs.MAIN:
                setActiveTabComponent(
                    <h1>Welcome, user!</h1>
                );
                break;
        }
    }, [activeTab, requestUrl, refreshRequestBody ]);

    const removeCookies = () => {
        window.localStorage.removeItem('access');
        window.localStorage.removeItem('refresh');
    };

    return(
        <Layout className="site-layout-background">
            <Header className="navbar-layout-background" >
                <div className='navbar-content'>
                    <Button className='phases-button'>
                        Assessment Phases
                    </Button>
                    <Select defaultValue={years[0]} style={{ width: 120 }} onChange={handleYearChange}>
                        {years.map(year => (
                            <Option key={year}>{year}</Option>
                        ))}
                    </Select>
                    <Select style={{ width: 120 }} value={phase} onChange={onPhaseChange}>
                        {phases.map(assessPhase => (
                            <Option key={assessPhase}>{assessPhase}</Option>
                        ))}
                    </Select>
                    <Link to='/login' style={{ textDecoration: 'none' }}>
                        <Button className='logout-button' type="link" onClick={removeCookies}>
                            Log Out
                        </Button>
                    </Link>
                </div>
            </Header>
            <Layout>
                <SideBar changeActiveTab={changeActiveTab}>
                </SideBar>
            </Layout>
            <Layout>
                <Content className='page-content' style={{ marginTop: '10vh'}}>
                    <h1>Welcome!</h1>
                </Content>
            </Layout>
        </Layout>
    )
};

export default UserPortal;