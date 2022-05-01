import React from 'react';
import {Modal, Form, InputNumber, Select, DatePicker, Tooltip} from 'antd';
import {InfoCircleFilled} from "@ant-design/icons";
import moment from 'moment';

const {RangePicker} = DatePicker;

const dateFormat = 'YYYY-MM-DD';

const WindowCreateForm = ({visible, onCreate, onCancel}) => {
    const [form] = Form.useForm();
    return (
        <Modal
            visible={visible}
            title="Create a new assessment week"
            okText="Create"
            cancelText="Cancel"
            onCancel={onCancel}
            onOk={() => {
                form
                    .validateFields()
                    .then((values) => {
                        form.resetFields();
                        onCreate(values);
                    })
                    .catch((info) => {
                        console.log('Validate Failed:', info);
                    });
            }}
        >
            <Form
                form={form}
                layout="vertical"
                name="form_in_modal"
                initialValues={{
                    modifier: 'public',
                    timeFrame: [moment(), moment()],
                    blockLength: 180
                }}
            >
                <Form.Item
                    name="timeFrame"
                    label="Time frame of the assessment week"
                    rules={[
                        {
                            required: true,
                            message: 'Please select the time frame of the assessment week!',
                        },
                    ]}
                >
                    <RangePicker
                        format={dateFormat}
                    />
                </Form.Item>

                <Tooltip title="Not editable yet." placement="bottomLeft">
                    <Form.Item
                    name="blockLength"
                    label="Duration of each block in minutes"
                    rules={[
                        {
                            required: true,
                            message: 'Please select the duration of each block!',
                        },
                    ]}
                >
                    <InputNumber disabled min={60}/>
                </Form.Item>
                </Tooltip>
            </Form>
        </Modal>
    );
};

export default WindowCreateForm;
