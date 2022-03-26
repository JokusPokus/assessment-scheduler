import React from "react";
import { Menu } from "antd";

const SideMenu = ({ changeActiveTab }) => {
    return (
        <Menu
          defaultSelectedKeys={['1']}
          mode='inline'
          theme='light'
          style={{ height: '100%', borderRight: 0 }}
        >
            <Menu.Item key="1">
                <p onClick={changeActiveTab('main')}>Main</p>
            </Menu.Item>
        </Menu>
    )
};

export default SideMenu;
