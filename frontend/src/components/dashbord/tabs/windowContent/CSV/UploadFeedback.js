import React from 'react';
import {Result, Button, Typography} from 'antd';
import {CloseCircleOutlined, RocketOutlined, FrownOutlined} from '@ant-design/icons';
import './UploadFeedback.css';

const {Paragraph, Text} = Typography;

const UploadError = ({uploadErrors}) => {
    return (
        <Result
            className="fade-in"
            icon={<FrownOutlined/>}
            title="The sheet was not as expected"
            subTitle="Please solve the following problems and upload again"
        >
            <div className="desc">
                {'missingCols' in uploadErrors &&
                <Paragraph>
                    <CloseCircleOutlined style={{color: 'red'}}/>&nbsp;&nbsp;&nbsp;The following required
                    columns are missing: <strong>{uploadErrors.missingCols.join(', ')}</strong>.
                </Paragraph>
                }
                {'wrongEmailCols' in uploadErrors &&
                <Paragraph>
                    <CloseCircleOutlined style={{color: 'red'}}/>&nbsp;&nbsp;&nbsp;The following
                    columns need to contain CODE email addresses only: <strong>{uploadErrors.wrongEmailCols.join(', ')}</strong>.
                </Paragraph>
                }
            </div>
        </Result>
    );
};

const UploadSuccess = ({windowStep, setWindowStep, setDisplaySuccess, setUploadSuccess}) => {
    const onReplaceRequest = () => {
        setDisplaySuccess(false);
        setUploadSuccess(false);
    };

    return (
        <Result
            className="fade-in steps-success"
            icon={<RocketOutlined/>}
            title="Successfully uploaded planning sheet!"
            extra={[
                <Button
                    key="replace"
                    shape="round"
                    size="large"
                    style={{marginRight: "20px"}}
                    onClick={() => onReplaceRequest()}
                >
                    Replace CSV
                </Button>,
                <Button
                    type="primary"
                    key="console"
                    shape="round"
                    size="large"
                    onClick={() => setWindowStep(windowStep + 1)}
                >
                    Next step
                </Button>,
            ]}
        />
    )
};

export {UploadError, UploadSuccess};
