import React, {useState} from 'react';
import {Empty, Button} from "antd";
import WindowForm from "./WindowForm";

const WindowAdder = ({onWindowCreate}) => {
    const [visible, setVisible] = useState(false);
    const [confirmLoading, setConfirmLoading] = useState(false);

    const onCreate = async (values) => {
        setConfirmLoading(true);
        await onWindowCreate(values);
        setConfirmLoading(false);
        setVisible(false);
    };

    return (
        <Empty
            imageStyle={{height: 300}}
            description={<span>No windows yet...</span>}
            style={{marginTop: "8%"}}
        >
            <Button
                type="primary"
                onClick={() => {
                    setVisible(true);
                }}
            >
                Add first window
            </Button>
            <WindowForm
                visible={visible}
                onConfirm={onCreate}
                onCancel={() => {
                    setVisible(false);
                }}
                type='create'
                confirmLoading={confirmLoading}
            />
        </Empty>
    );
};

export default WindowAdder;
