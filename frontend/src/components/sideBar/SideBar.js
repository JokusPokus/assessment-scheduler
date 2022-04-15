import React from "react";
import { Layout } from "antd";
import './SideBar.css'
import SideMenu from "./SideMenu";

const SideBar = ({changeActiveTab}) => {
  return (
    <Layout.Sider
      className="sidebar"
      breakpoint={"lg"}
      collapsedWidth={0}
      trigger={null}
      width={220}
    >
        <SideMenu style={{height: "100vh"}} changeActiveTab={changeActiveTab}/>
    </Layout.Sider>
   );
};
export default SideBar;