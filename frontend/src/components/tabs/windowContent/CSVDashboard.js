import React, {useState} from 'react';
import {Upload, Form, Button, Result} from 'antd';
import {InboxOutlined} from '@ant-design/icons';
import {httpPostPlanningSheet} from "../../../hooks/requests";
import "./WindowSteps.css"

const {Dragger} = Upload;

const CSVDashboard = ({window, windowStep, setWindowStep, uploadSuccess, setUploadSuccess}) => {

    const [isUploading, setIsUploading] = useState(false);
    const [form] = Form.useForm();

    const onFinish = async (values) => {
        setIsUploading(true);
        const response = await httpPostPlanningSheet(
            {
                csv: values.planningSheet[0].originFileObj,
                window: window.id
            }
        );
        setTimeout(() => {
            if (response.status === 200) {
                setUploadSuccess(true);
            }
            setIsUploading(false);
        }, 1000);

    };

    const normFile = (event) => {
        if (Array.isArray(event)) {
            return event
        }

        if (event.fileList.length > 1) {
            event.fileList.shift();
        }
        return event && event.fileList
    };

    const dummyRequest = ({file, onSuccess}) => {
        setTimeout(() => {
            onSuccess("ok");
        }, 0);
    };

    return (
        <>
            {uploadSuccess ? (
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
            ) : (
                <Form
                    form={form}
                    layout="vertical"
                    name="upload_form"
                    onFinish={onFinish}
                    initialValues={{
                        modifier: 'public',
                    }}
                    encType="multipart/form-data"
                    style={{
                        width: "50%",
                        margin: "auto"
                    }}
                >
                    <Form.Item>
                        <Form.Item
                            name="planningSheet"
                            valuePropName="fileList"
                            getValueFromEvent={normFile}
                            noStyle
                        >
                            <Upload.Dragger
                                name="files"
                                customRequest={dummyRequest}
                                multiple={false}
                                accept=".csv"
                                style={{padding: "10%"}}
                            >
                                <p className="ant-upload-drag-icon">
                                    <InboxOutlined/>
                                </p>
                                <p className="ant-upload-text">Click or drag CSV file to this area to upload</p>
                            </Upload.Dragger>
                        </Form.Item>
                    </Form.Item>
                    <Form.Item
                        wrapperCol={{
                            span: 12,
                            offset: 6,
                        }}
                        shouldUpdate
                    >
                        {() => (
                            <Button
                                type="primary"
                                htmlType="submit"
                                loading={isUploading}
                                disabled={!form.getFieldValue("planningSheet")}
                            >
                                Upload
                            </Button>
                        )}
                    </Form.Item>
                </Form>
            )}
        </>
    );
};

export default CSVDashboard;