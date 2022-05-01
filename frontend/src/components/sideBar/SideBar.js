import React from "react";
import { Layout } from "antd";
import './SideBar.css'
import SideMenu from "./SideMenu";

const SideBar = () => {
  return (
    <Layout.Sider
      className="sidebar"
      breakpoint={"lg"}
      collapsedWidth={0}
      trigger={null}
      width={150}
    >
        <SideMenu style={{height: "100vh"}} />
    </Layout.Sider>
   );
};
export default SideBar;