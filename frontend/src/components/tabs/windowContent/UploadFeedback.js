import React from 'react';
import {Result, Button, Typography} from 'antd';
import {CloseCircleOutlined} from '@ant-design/icons';

const {Paragraph, Text} = Typography;

const UploadError = ({missingColumns}) => {
    return (
        <Result
            status="error"
            title="Upload Failed"
            subTitle="Please check and modify the following information before resubmitting."
        >
            <div className="desc" style={{textAlign: 'left'}}>
                <Paragraph>
                    <Text
                        strong
                        style={{
                            fontSize: 16,
                        }}
                    >
                        The content you submitted has the following error:
                    </Text>
                </Paragraph>
                {missingColumns &&
                <Paragraph>
                    <CloseCircleOutlined style={{color: 'red'}}/> The following required
                    columns are missing:
                    <ul style={{marginLeft: '20px'}}>
                        {missingColumns.map(colName => <li><strong>{colName}</strong></li>)}
                    </ul>
                </Paragraph>
                }
            </div>
        </Result>
    );
};

const UploadSuccess = ({windowStep, setWindowStep}) => {
    return (
        <Result
            className="uploadSuccessFeedback"
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
