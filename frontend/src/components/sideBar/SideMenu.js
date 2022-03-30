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
          defaultSelectedKeys={['1']}
          mode='inline'
          theme='dark'
          style={{ height: '100%', borderRight: 0, fontSize: '16px' }}
        >
            <Menu.Item key="1" style={{ marginTop: "65px"}}>
                <p onClick={changeActiveTab('dashboard')}>Dashboard</p>
            </Menu.Item>
            <Menu.Item key="2">
                <p onClick={changeActiveTab('weeks')}>Weeks</p>
            </Menu.Item>
            <Menu.Item key="3">
                <p onClick={changeActiveTab('avail')}>Availabilities</p>
            </Menu.Item>
            <Menu.Item key="4">
                <p onClick={changeActiveTab('rooms')}>Rooms</p>
            </Menu.Item>
            <Menu.Item key="5">
                <p onClick={changeActiveTab('modules')}>Modules</p>
            </Menu.Item>
            <Menu.Item key="6">
                <p onClick={changeActiveTab('assessments')}>Assessments</p>
            </Menu.Item>
            <Menu.Item key="7">
                <p onClick={changeActiveTab('schedules')}>Schedules</p>
            </Menu.Item>
            <Menu.Item
                key="8"
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
