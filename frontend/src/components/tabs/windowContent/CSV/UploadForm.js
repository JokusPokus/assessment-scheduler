import {Button, Form, Upload} from "antd";
import {InboxOutlined} from "@ant-design/icons";
import React from "react";


const UploadForm = ({onFinish, isUploading}) => {
    const [form] = Form.useForm();

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
        <Form
            form={form}
            layout="vertical"
            name="upload_form"
            onFinish={onFinish}
            initialValues={{
                modifier: 'public',
            }}
            encType="multipart/form-data"
            style={{margin: "auto"}}
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
    );
};

export default UploadForm;
