import React from 'react';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Button, Layout, Menu, Dropdown } from 'antd';
import { DownOutlined } from '@ant-design/icons';
import './Portal.css'
import SideBar from '../../components/sideBar/SideBar';

const { Header, Content, Footer } = Layout;
const { SubMenu } = Menu;

const UserPortal = ({ requestUrl, refreshRequestBody }) => {
    const [activeTab, setActiveTab] = useState('main');
    const [visible, setVisible] = useState(false);

    const changeActiveTab = (tabName) => {
        return (event) => {
            setActiveTab(tabName);
            setVisible(false)
        }
    };

    const [activeTabComponent, setActiveTabComponent] = useState(
        <h1>Welcome, user!</h1>
    );

    const PHASES = [
        {name: "FS 2021", id: "fs21", weeks: ["Week 1", "Week 2", "Week 3"]},
        {name: "SS 2022", id: "ss22", weeks: ["Week 1", "Week 2", "Week 3"]},
        {name: "FS 2022", id: "fs22", weeks: ["Week 1", "Week 2", "Week 3"]},
    ];

    const menu = (
        <Menu>
            {PHASES.map((phase, index) => (
                <SubMenu title={phase.name} key={phase.name}>
                    {phase.weeks.map((week, w_index) => (
                        <Menu.Item key={`${phase.name}_${week}`}>{week}</Menu.Item>)
                    )}
                </SubMenu>
            ))}
        </Menu>
    );

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
    }, [activeTab, requestUrl, refreshRequestBody ])

    const removeCookies = () => {
            window.localStorage.removeItem('access');
            window.localStorage.removeItem('refresh');
    };

    return(
        <Layout className="site-layout-background">
            <Header className="navbar-layout-background" >
                <div className='navbar-content'>
                    <Link to='/phases' style={{ textDecoration: 'none' }}>
                        <Button className='phases-button' type="link">
                            Assessment Phases
                        </Button>
                    </Link>
                    <Link to='/login' style={{ textDecoration: 'none' }}>
                        <Button className='logout-button' type="link" onClick={removeCookies}>
                            Log Out
                        </Button>
                    </Link>
                </div>
            </Header>
            <Content className='page-content'>
                <Layout className='content_layout'>
                    <SideBar changeActiveTab={changeActiveTab}/>
                    <Content className="site-layout-background rendered-content">
                        {activeTabComponent}
                    </Content>
                </Layout>
            </Content>
            <Footer className="site-layout-background" style={{ textAlign: 'center' }}>CODE assessment scheduler</Footer>
        </Layout>
    )
};

export default UserPortal;