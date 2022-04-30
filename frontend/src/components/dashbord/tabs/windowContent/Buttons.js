import React from 'react';
import {Button} from "antd";


export const NextStepButton = ({windowStep, setWindowStep, status}) => {
    return (
        status === "success" && (
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