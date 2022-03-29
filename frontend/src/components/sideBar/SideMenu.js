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
                <p onClick={changeActiveTab('main')}>Main</p>
            </Menu.Item>
            <Menu.Item key="2">
                <p onClick={changeActiveTab('second')}>Second</p>
            </Menu.Item>
        </Menu>
    )
};

export default SideMenu;
