import React from "react";
import {Menu, Space} from "antd";
import {Link} from "react-router-dom";
import {LogoutOutlined} from "@ant-design/icons";

const SideMenu = ({ changeActiveTab }) => {
    const removeCookies = () => {
        window.localStorage.removeItem('access');
        window.localStorage.removeItem('refresh');
    };

    return (
        <Menu
          mode='inline'
          theme='dark'
          style={{ height: '100%', borderRight: 0, fontSize: '16px', width: '150px' }}
        >
            <Menu.Item
                key="2"
                style={{
                    position: 'absolute',
                    bottom: '20px',
                    zIndex: 1,
                    transition: 'all 0.2s',
                }}
                icon={<LogoutOutlined />}
            >
                <Link to="/login" onClick={removeCookies}>
                    <p>Log out</p>
                </Link>
            </Menu.Item>
        </Menu>
    )
};

export default SideMenu;
