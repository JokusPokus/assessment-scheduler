import React from 'react';
import {Button} from "antd";
import {CheckOutlined, WarningOutlined} from "@ant-design/icons";


const processStatus = {
        INITIAL: "initial",
        LOADING: "loading",
        SUCCESS: "success",
        FAILURE: "failure"
    };


export const NextStepButton = ({windowStep, setWindowStep, status}) => {
    return (
        status === processStatus.SUCCESS && (
            <Button
                type="primary"
                shape="round"
                size="large"
                style={{
                    marginTop: "30px",
                    marginBottom: "30px",
                    marginRight: "20px",
                    float: "right"
                }}
                key="console"
                onClick={() => setWindowStep(windowStep + 1)}
            >
                <strong>Next step</strong>
            </Button>
        )
    );
};


export const SaveButton = ({onClick, status, disabled, title}) => {
    return (
        <Button
            type="primary"
            shape="round"
            size="large"
            style={{
                marginTop: "30px",
                marginBottom: "30px",
                marginRight: "20px",
                float: "right"
            }}
            onClick={onClick}
            loading={status === processStatus.LOADING}
            disabled={disabled}
            icon={status === processStatus.SUCCESS
                ? <strong><CheckOutlined/> </strong>
                : status === processStatus.FAILURE
                    ? <strong><WarningOutlined/> </strong>
                    : null
            }
        >
            <strong>{title}</strong>
        </Button>
    );
};
