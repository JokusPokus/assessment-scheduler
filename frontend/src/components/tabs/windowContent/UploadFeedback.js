import React from 'react';
import {Result, Button, Typography} from 'antd';
import {CloseCircleOutlined} from '@ant-design/icons';
import './UploadFeedback.css';

const {Paragraph, Text} = Typography;

const UploadError = ({missingColumns}) => {
    return (
        <Result
            status="error"
            title="The sheet was not as expected"
        >
            <div className="desc">
                {missingColumns &&
                <Paragraph>
                    <CloseCircleOutlined style={{color: 'red'}}/>&nbsp;&nbsp;&nbsp;The following required
                    columns are missing: <strong>{missingColumns.join(', ')}</strong>.
                </Paragraph>
                }
            </div>
        </Result>
    );
};

const UploadSuccess = ({windowStep, setWindowStep}) => {
    return (
        <Result
            className="uploadSuccessFeedback steps-success"
            status="success"
            title="Successfully uploaded planning sheet!"
            extra={[
                <Button
                    type="primary"
                    key="console"
                    onClick={() => setWindowStep(windowStep + 1)}
                >
                    Next step
                </Button>,
            ]}
        />
    )
};

export {UploadError, UploadSuccess};
