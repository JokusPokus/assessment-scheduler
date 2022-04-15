import React from 'react';
import {Result, Button, Typography} from 'antd';
import {CloseCircleOutlined} from '@ant-design/icons';
import './UploadFeedback.css';

const {Paragraph, Text} = Typography;

const UploadError = ({missingColumns}) => {
    return (
        <Result
            className="uploadFeedback"
            status="error"
            title="The sheet was not as expected"
            subTitle="Please solve the following problems and upload again"
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
            className="uploadFeedback steps-success"
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
