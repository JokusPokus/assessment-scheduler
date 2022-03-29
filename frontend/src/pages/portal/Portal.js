import React from 'react';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Layout, Select } from 'antd';
import './Portal.css'
import SideBar from '../../components/sideBar/SideBar';
import PortalHeader from "../../components/header/PortalHeader";

const { Header, Content, Footer } = Layout;
const { Option } = Select;

const UserPortal = ({ requestUrl, refreshRequestBody }) => {
    const [activeTab, setActiveTab] = useState('main');
    const [activeTabComponent, setActiveTabComponent] = useState(
        <h1>Welcome, user!</h1>
    );

    const changeActiveTab = (tabName) => {
        return (event) => {
            setActiveTab(tabName);
        }
    };

    useEffect(() => {
        const tabs = {
            MAIN: "main",
            SECOND: "second"
        };

        switch (activeTab) {
            case tabs.MAIN:
                setActiveTabComponent(
                    <h1>Welcome, user!</h1>
                );
                break;
            case tabs.SECOND:
                setActiveTabComponent(
                    <h1>This is another tab!</h1>
                );
                break;
        }
    }, [activeTab, requestUrl, refreshRequestBody ]);

    const phaseData = {
        2022: ["Spring Semester", "Fall Semester"],
        2021: ["Fall Semester"],
    };
    const years = Object.keys(phaseData);

    const [phases, setPhases] = useState(phaseData[years[0]]);
    const [phase, setPhase] = useState(phaseData[years[0]][0]);

    return(
        <Layout className="site-layout-background" style={{ minHeight: "100vh" }}>
            <SideBar changeActiveTab={changeActiveTab}/>
            <Layout>
                <PortalHeader
                    phase={phase}
                    setPhase={setPhase}
                    phases={phases}
                    setPhases={setPhases}
                    phaseData={phaseData}
                />
                <Content className='page-content'>
                    { activeTabComponent }
                </Content>
            </Layout>
        </Layout>
    )
};

export default UserPortal;