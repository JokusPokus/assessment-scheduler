import React from 'react';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Button, Layout } from 'antd';
import SideBar from '../../components/sideBar/SideBar';

const { Header, Content, Footer } = Layout;

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