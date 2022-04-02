import {Tabs} from 'antd';
import React, {useState} from "react";

const {TabPane} = Tabs;

const WindowTabs = () => {
    const initialPanes = [
        {
            title: 'Week 1',
            content: 'Content of Week 1',
            key: '1',
        },
    ];
    const [panes, setPanes] = useState(initialPanes);
    const [activeKey, setActiveKey] = useState(initialPanes[0].key);

    const onChange = paneKey => {
        setActiveKey(paneKey);
    };

    const add = () => {
        const currentMaxKey = parseInt(panes.slice(-1)[0].key);
        const newKey = (currentMaxKey + 1).toString();
        console.log(newKey)
        const newPane = {
            title: `Week ${newKey}`,
            content: 'New content',
            key: newKey
        };
        setPanes([...panes, newPane]);
        setActiveKey(newKey);
    };

    const onEdit = (targetKey, action) => {
        eval(action)(targetKey);
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
        </div>
    );
};

export default WindowTabs;
