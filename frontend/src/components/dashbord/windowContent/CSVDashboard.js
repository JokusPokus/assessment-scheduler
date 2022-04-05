import React from 'react';
import {Upload, message, Form, Button} from 'antd';
import {InboxOutlined} from '@ant-design/icons';
import {httpPostPlanningSheet} from "../../../hooks/requests";

const {Dragger} = Upload;

const CSVDashboard = ({window}) => {
    const [form] = Form.useForm();

    const onFinish = async (values) => {
        requestBody = {
            planning_sheet: values.planningSheet,
            window: window.id
        };
        await httpPostPlanningSheet()
    };

    const dummyRequest = ({file, onSuccess}) => {
        setTimeout(() => {
            onSuccess("ok");
        }, 0);
    };

    const normFile = (e) => {
        if (Array.isArray(e)) {
            return e;
        }

        return e && e.fileList[0];
    };

    return (
        <>
            <Form
                form={form}
                layout="vertical"
                name="upload_form"
                onFinish={onFinish}
                initialValues={{
                    modifier: 'public',
                }}
            >
                <Form.Item>
                    <Form.Item name="planningSheet" valuePropName="fileList" getValueFromEvent={normFile} noStyle>
                        <Upload.Dragger name="files" customRequest={dummyRequest} multiple={false}>
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
                >
                    <Button type="primary" htmlType="submit">
                        Upload
                    </Button>
                </Form.Item>
            </Form>
        </>
    );
};

export default CSVDashboard;