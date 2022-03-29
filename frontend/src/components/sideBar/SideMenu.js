import React from "react";
import { Menu } from "antd";

const SideMenu = ({ changeActiveTab }) => {
    return (
        <Menu
          defaultSelectedKeys={['1']}
          mode='inline'
          theme='dark'
          style={{ height: '100%', borderRight: 0 }}
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
        </Menu>
    )
};

export default SideMenu;
