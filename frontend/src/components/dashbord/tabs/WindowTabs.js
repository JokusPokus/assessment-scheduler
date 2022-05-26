import React, {useState, useEffect} from "react";
import {message, Tabs} from 'antd';
import {EditOutlined} from "@ant-design/icons";
import WindowForm from "../WindowForm";
import WindowContent from "./windowContent/WindowContent";
import {httpDeleteWindow, httpPatchWindow, httpPostModuleDurations} from "../../../hooks/requests";

const {TabPane} = Tabs;
const _ = require('lodash');

const WindowTabs = ({currentPhase, onWindowCreate, setPhaseData}) => {
    const [panes, setPanes] = useState([]);
    const [phaseId, setPhaseId] = useState(undefined);
    const [activeKey, setActiveKey] = useState(undefined);
    const [paneToBeModified, setPaneToBeModified] = useState(null);
    const [addFormVisible, setAddFormVisible] = useState(false);
    const [confirmLoading, setConfirmLoading] = useState(false);

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
        setAddFormVisible(true);
    };

    const remove = async (targetKey) => {
        const pos = targetKey.split("_")[1];
        const index = panes.findIndex(pane => pane.position.toString() === pos);
        setPaneToBeModified(panes[index]);
    };

    const onEdit = (targetKey, action) => {
        eval(action)(targetKey);
    };

    const onCreate = async (values) => {
        setConfirmLoading(true);
        await onWindowCreate(values);
        setActiveKey(`${phaseId}_${(panes.length + 1).toString()}`);
        setConfirmLoading(false);
        setAddFormVisible(false);
    };

    const onModify = async (values) => {
        const requestBody = {
            start_date: values.timeFrame[0].format('YYYY-MM-DD'),
            end_date: values.timeFrame[1].format('YYYY-MM-DD'),
            block_length: values.blockLength
        };
        setConfirmLoading(true);
        setTimeout(async () => {
            const response = await httpPatchWindow(paneToBeModified.id, requestBody)();
            if (response.status === 200) {
                message.success(`You successfully updated week ${paneToBeModified.position}.`);
                await setPhaseData();
            } else {
                message.error("Something went wrong...");
            }
            setPaneToBeModified(null);
            setConfirmLoading(false);
        }, 1000);
    };

    const onDelete = async (targetKey) => {
        setConfirmLoading(true);
        setTimeout(async () => {
            const response = await httpDeleteWindow(paneToBeModified.id)();
            if (response.status === 204) {
                message.success(`You successfully deleted week ${paneToBeModified.position}.`);
                await setPhaseData();
            } else {
                message.error("Something went wrong...");
            }
            setPaneToBeModified(null);
            setConfirmLoading(false);
        }, 1000);
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
                        <TabPane
                            tab={`Week ${pane.position}`}
                            key={`${phaseId}_${pane.position}`}
                            closable={true}
                            closeIcon={<EditOutlined/>}
                        >
                            <WindowContent phase={currentPhase} window={pane} setPhaseData={setPhaseData}/>
                        </TabPane>
                    ))}
                </Tabs>
                < WindowForm
                    visible={addFormVisible}
                    onConfirm={onCreate}
                    onCancel={() => {
                        setAddFormVisible(false);
                    }}
                    type='create'
                    confirmLoading={confirmLoading}
                />
                < WindowForm
                    visible={paneToBeModified !== null}
                    onConfirm={onModify}
                    onDelete={onDelete}
                    onCancel={() => {
                        setPaneToBeModified(null);
                    }}
                    type='modify'
                    confirmLoading={confirmLoading}
                    paneToBeModified={paneToBeModified}
                />
            </>}
        </div>
    );
};

export default WindowTabs;
