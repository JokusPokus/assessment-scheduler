import React from 'react';
import {useState, useEffect} from 'react';
import {Layout} from 'antd';
import './Portal.css'
import SideBar from '../../components/sideBar/SideBar';
import PortalHeader from "../../components/header/PortalHeader";
import Dashboard from "../../components/dashbord/Dashboard";

import {httpGetPhase, httpGetUser} from "../../hooks/requests";


const {Header, Content, Footer} = Layout;

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

    const setPhaseData = async (year = currentYear, semester = currentSemester) => {
        const response = await httpGetPhase({year: year, semester: semester})();
        setCurrentPhase(await response.json());
    };

    useEffect(async () => {
        if (currentSemester) {
            await setPhaseData(currentYear, currentSemester);
        }
    }, [currentSemester, currentYear, newWindowCounter]);

    return (
        <Layout className="site-layout-background" style={{minHeight: "100vh"}}>
            <SideBar/>
            <Layout>
                <PortalHeader
                    currentYear={currentYear}
                    setCurrentYear={setCurrentYear}
                    currentSemester={currentSemester}
                    setCurrentSemester={setCurrentSemester}
                    userInfo={userInfo}
                />
                <Content className='page-content'>
                    <Dashboard
                        currentPhase={currentPhase}
                        newWindowCounter={newWindowCounter}
                        setNewWindowCounter={setNewWindowCounter}
                        setPhaseData={setPhaseData}
                    />
                </Content>
            </Layout>
        </Layout>
    )
};

export default UserPortal;