import React from 'react';
import { Modal, Form, InputNumber, Select } from 'antd';

const { Option } = Select;

const PhaseCreateForm = ({visible, onCreate, onCancel}) => {
    const [form] = Form.useForm();
    return (
        <Modal
            visible={visible}
            title="Create a new assessment phase"
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
                    year: new Date().getFullYear(),
                    semester: "Spring Semester"
                }}
            >
                <Form.Item
                    name="year"
                    label="Year"
                    rules={[
                        {
                            required: true,
                            message: 'Please input the calendar year!',
                        },
                    ]}
                >
                    <InputNumber min={2022}/>
                </Form.Item>
                <Form.Item
                    name="semester"
                    label="Semester"
                    rules={[
                        {
                            required: true,
                            message: 'Please input the semester!',
                        },
                    ]}
                >
                    <Select>
                        <Option value="spring">Spring Semester</Option>
                        <Option value="fall">Fall Semester</Option>
                    </Select>
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default PhaseCreateForm;
