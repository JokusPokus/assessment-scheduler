import {Tabs} from 'antd';
import React, {useState, useEffect} from "react";
import WindowCreateForm from "../WindowCreateForm";
import WindowContent from "./windowContent/WindowContent";

const {TabPane} = Tabs;
const _ = require('lodash');

const WindowTabs = ({currentPhase, onWindowCreate, setPhaseData}) => {
    const [panes, setPanes] = useState([]);
    const [phaseId, setPhaseId] = useState(undefined);
    const [activeKey, setActiveKey] = useState(undefined);
    const [visible, setVisible] = useState(false);

    useEffect(() => {
        if (!_.isEmpty(currentPhase)) {
            setPanes(currentPhase.windows);
            if (currentPhase.id !== phaseId) {
                setActiveKey(`${currentPhase.id}_1`);
                setPhaseId(currentPhase.id);
            }
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
        setActiveKey(`${phaseId}_${(panes.length + 1).toString()}`);
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
                    size={"large"}
                >
                    {panes.map(pane => (
                        <TabPane tab={`Week ${pane.position}`} key={`${phaseId}_${pane.position}`} closable={false}>
                            <WindowContent window={pane} setPhaseData={setPhaseData}/>
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
