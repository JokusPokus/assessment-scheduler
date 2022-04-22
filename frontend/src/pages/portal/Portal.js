import React from 'react';
import {useState, useEffect} from 'react';
import {Link} from 'react-router-dom';
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

import {httpGetPhase, httpGetPhases, httpGetUser} from "../../hooks/requests";
import usePhases from "../../hooks/callbacks";


const {Header, Content, Footer} = Layout;
const {Option} = Select;

const UserPortal = ({requestUrl, refreshRequestBody}) => {
    const [currentPhase, setCurrentPhase] = useState({});
    const [userInfo, setUserInfo] = useState(undefined);
    const [currentYear, setCurrentYear] = useState(undefined);
    const [currentSemester, setCurrentSemester] = useState(undefined);
    const [newWindowCounter, setNewWindowCounter] = useState(0);
    const [activeTab, setActiveTab] = useState('dashboard');
    const [activeTabComponent, setActiveTabComponent] = useState(
        <Dashboard currentPhase={currentPhase}/>
    );

    useEffect(async () => {
        const response = await httpGetUser()
        setUserInfo(await response.json());
    }, []);

    const setPhaseData = async (year, semester) => {
        const response = await httpGetPhase({year: year, semester: semester})();
        setCurrentPhase(await response.json());
    };

    useEffect(async () => {
        if (currentSemester) {
            await setPhaseData(currentYear, currentSemester);
        }
    }, [currentSemester, currentYear, newWindowCounter]);

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
                setActiveTabComponent(
                    <Dashboard
                        currentPhase={currentPhase}
                        newWindowCounter={newWindowCounter}
                        setNewWindowCounter={setNewWindowCounter}
                    />
                );
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
    }, [activeTab, requestUrl, refreshRequestBody, currentPhase]);

    return (
        <Layout className="site-layout-background" style={{minHeight: "100vh"}}>
            <SideBar changeActiveTab={changeActiveTab}/>
            <Layout>
                <PortalHeader
                    currentYear={currentYear}
                    setCurrentYear={setCurrentYear}
                    currentSemester={currentSemester}
                    setCurrentSemester={setCurrentSemester}
                    userInfo={userInfo}
                />
                <Content className='page-content'>
                    {activeTabComponent}
                </Content>
            </Layout>
        </Layout>
    )
};

export default UserPortal;