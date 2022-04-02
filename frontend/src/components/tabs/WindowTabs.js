import {Tabs} from 'antd';
import React, {useState} from "react";
import WindowCreateForm from "../dashbord/WindowCreateForm";

const {TabPane} = Tabs;

const WindowTabs = ({onWindowCreate}) => {
    const initialPanes = [
        {
            title: 'Week 1',
            content: 'Content of Week 1',
            key: '1',
        },
    ];
    const [panes, setPanes] = useState(initialPanes);
    const [activeKey, setActiveKey] = useState(initialPanes[0].key);
    const [visible, setVisible] = useState(false);

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
        const currentMaxKey = parseInt(panes.slice(-1)[0].key);
        const newKey = (currentMaxKey + 1).toString();
        const newPane = {
            title: `Week ${newKey}`,
            content: 'New content',
            key: newKey
        };
        setPanes([...panes, newPane]);
        setActiveKey(newKey);
        setVisible(false);
    };

    return (
        <div className="card-container">
            <Tabs
                type="editable-card"
                onEdit={onEdit}
                activeKey={activeKey}
                onChange={onChange}
            >
                {panes.map(pane => (
                    <TabPane tab={pane.title} key={pane.key} closable={false}>
                        {pane.content}
                    </TabPane>
                ))}
            </Tabs>
            <WindowCreateForm
                visible={visible}
                onCreate={onCreate}
                onCancel={() => {
                    setVisible(false);
                }}
            />
        </div>
    );
};

export default WindowTabs;
