import {Tabs} from 'antd';
import React, {useState, useEffect} from "react";
import WindowCreateForm from "../dashbord/WindowCreateForm";
import WindowContent from "../dashbord/WindowContent";

const {TabPane} = Tabs;
const _ = require('lodash');

const WindowTabs = ({currentPhase, onWindowCreate}) => {
    const [panes, setPanes] = useState([]);
    const [activeKey, setActiveKey] = useState("1");
    const [visible, setVisible] = useState(false);

    useEffect(() => {
        if (!_.isEmpty(currentPhase)) {
            setPanes(currentPhase.windows);
        }
    }, [currentPhase]);

    const onChange = paneKey => {
        setActiveKey(paneKey);
    };

    const add = async () => {
        setVisible(true);
    };

    const onEdit = (targetKey, action) => {
        eval(action)(targetKey);
    };

    const onCreate = async (values) => {
        await onWindowCreate(values);
        setActiveKey((panes.length + 1).toString());
        setVisible(false);
    };

    return (
        <div className="card-container">
            {panes.length !== 0 &&
            <>
                <Tabs
                    type="editable-card"
                    onEdit={onEdit}
                    activeKey={activeKey}
                    onChange={onChange}
                >
                    {panes.map(pane => (
                        <TabPane tab={`Week ${pane.position}`} key={pane.position.toString()} closable={false}>
                            <WindowContent window={pane}/>
                        </TabPane>
                    ))}
                </Tabs>
                < WindowCreateForm
                    visible={visible}
                    onCreate={onCreate}
                    onCancel={() => {
                        setVisible(false);
                    }}
                />
            </>}
        </div>
    );
};

export default WindowTabs;
