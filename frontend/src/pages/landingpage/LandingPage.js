import React from 'react';
import { Layout } from 'antd';
import { Header } from 'antd/lib/layout/layout';
import { Link } from 'react-router-dom';

const LandingPage = () => {
    return(
        <Layout className="site-layout-background">
            <Header className="header navbar-layout-background" >
                <div className='navbar-content'>
                    <div className='logo-area'>
                        <Link to='/' style={{ textDecoration: 'none' }}>
                            <h1>FairVote</h1>
                        </Link>
                    </div>
                </div>
            </Header>
            <div>Landing Page</div>
        </Layout>
    )
};

export default LandingPage;
