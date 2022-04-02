import React, {useState} from 'react';
import {Empty, Button} from "antd";
import {httpPostWindow} from "../../hooks/requests";
import WindowCreateForm from "./WindowCreateForm";

const WindowAdder = ({currentPhase, newWindowCounter, setNewWindowCounter}) => {
    const [visible, setVisible] = useState(false);

    const onCreate = async (values) => {
        const requestBody = {
            start_date: values.timeFrame[0].format('YYYY-MM-DD'),
            end_date: values.timeFrame[1].format('YYYY-MM-DD'),
            block_length: values.blockLength,
            assessment_phase: currentPhase.id
        };
        await httpPostWindow(requestBody)();
        setNewWindowCounter(newWindowCounter + 1);
        setVisible(false);
    };

    return (
        <Empty
            imageStyle={{height: 300}}
            description={<span>No weeks yet...</span>}
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
