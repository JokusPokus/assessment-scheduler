import React from 'react';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {Layout, message, Select} from 'antd';
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

import {httpGetPhases, httpGetUser} from "../../hooks/requests";
import usePhases from "../../hooks/callbacks";


const { Header, Content, Footer } = Layout;
const { Option } = Select;

const UserPortal = ({ requestUrl, refreshRequestBody }) => {
    const [currentPhase, setCurrentPhase] = useState(undefined);
    const [userInfo, setUserInfo] = useState(undefined);
    const [activeTab, setActiveTab] = useState('main');
    const [activeTabComponent, setActiveTabComponent] = useState(Dashboard);

    useEffect(() => {
        httpGetUser()
            .then(data => {
                setUserInfo(data);
            });
    }, []);

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

    return(
        <Layout className="site-layout-background" style={{ minHeight: "100vh" }}>
            <SideBar changeActiveTab={changeActiveTab}/>
            <Layout>
                <PortalHeader
                    currentPhase={currentPhase}
                    setCurrentPhase={setCurrentPhase}
                    userInfo={userInfo}
                />
                <Content className='page-content'>
                    { activeTabComponent }
                </Content>
            </Layout>
        </Layout>
    )
};

export default UserPortal;