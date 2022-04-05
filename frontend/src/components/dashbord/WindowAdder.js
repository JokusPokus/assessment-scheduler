import React, {useState} from 'react';
import {Empty, Button} from "antd";
import WindowCreateForm from "./WindowCreateForm";

const WindowAdder = ({onWindowCreate}) => {
    const [visible, setVisible] = useState(false);

    const onCreate = async (values) => {
        await onWindowCreate(values);
        setVisible(false);
    };

    return (
        <Empty
            imageStyle={{height: 300}}
            description={<span>No weeks yet...</span>}
            style={{marginTop: "8%"}}
        >
            <Button
                type="primary"
                onClick={() => {
                    setVisible(true);
                }}
            >
                Add first week
            </Button>
            <WindowCreateForm
                visible={visible}
                onCreate={onCreate}
                onCancel={() => {
                    setVisible(false);
                }}
            />
        </Empty>
    );
};

export default WindowAdder;
