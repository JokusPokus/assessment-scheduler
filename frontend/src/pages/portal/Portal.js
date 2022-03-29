import React from 'react';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Layout, Select } from 'antd';
import './Portal.css'
import SideBar from '../../components/sideBar/SideBar';
import PortalHeader from "../../components/header/PortalHeader";
import Dashboard from "../../components/dashbord/Dashboard";
import Weeks from "../../components/weeks/Weeks";
import Schedules from "../../components/schedules/Schedules";
import Modules from "../../components/modules/Modules";
import Availabilities from "../../components/availabilities/Availabilities";
import Assessments from "../../components/assessments/Assessments";
import Rooms from "../../components/rooms/Rooms";


const { Header, Content, Footer } = Layout;
const { Option } = Select;

const UserPortal = ({ requestUrl, refreshRequestBody }) => {
    const [activeTab, setActiveTab] = useState('main');
    const [activeTabComponent, setActiveTabComponent] = useState(Dashboard);

    const changeActiveTab = (tabName) => {
        return (event) => {
            setActiveTab(tabName);
        }
    };

    useEffect(() => {
        const tabs = {
            DASHBOARD: "dashboard",
            WEEKS: "weeks",
            AVAIL: "avail",
            ROOMS: "rooms",
            MODULES: "modules",
            ASSESSMENTS: "assessments",
            SCHEDULES: "schedules",
        };

        switch (activeTab) {
            case tabs.DASHBOARD:
                setActiveTabComponent(Dashboard);
                break;
            case tabs.WEEKS:
                setActiveTabComponent(Weeks);
                break;
            case tabs.AVAIL:
                setActiveTabComponent(Availabilities);
                break;
            case tabs.ROOMS:
                setActiveTabComponent(Rooms);
                break;
            case tabs.MODULES:
                setActiveTabComponent(Modules);
                break;
            case tabs.ASSESSMENTS:
                setActiveTabComponent(Assessments);
                break;
            case tabs.SCHEDULES:
                setActiveTabComponent(Schedules);
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