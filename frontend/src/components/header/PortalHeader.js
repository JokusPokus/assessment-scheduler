import React from "react";
import { Button, Layout } from "antd";
import { HomeOutlined } from '@ant-design/icons';
import PhaseSelector from "./PhaseSelector";


const PortalHeader = ({ currentPhase, setCurrentPhase, userInfo }) => {
    return (
        <Layout.Header className="navbar-layout-background" >
            <div className='navbar-content'>
                <PhaseSelector
                    currentPhase={currentPhase}
                    setCurrentPhase={setCurrentPhase}
                />
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
