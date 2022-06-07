import React, {useEffect} from 'react';
import {Modal, Form, InputNumber, DatePicker, Tooltip, Button} from 'antd';
import moment from 'moment';

const {RangePicker} = DatePicker;

const dateFormat = 'YYYY-MM-DD';

const WindowForm = ({
                        visible,
                        onConfirm,
                        onCancel,
                        type,
                        confirmLoading,
                        paneToBeModified = null,
                        onDelete = null
                    }) => {

    const title = {
        create: "Create a new assessment window",
        modify: `Modify assessment window ${paneToBeModified && paneToBeModified.position}`
    }[type];

    const okText = {
        create: "Create",
        modify: "Save"
    }[type];

    const timeFrame = paneToBeModified
        ? [moment(paneToBeModified.start_date), moment(paneToBeModified.end_date)]
        : [moment(), moment()];

    const blockLength = paneToBeModified
        ? paneToBeModified.block_length
        : 180;

    const deleteProps = type === 'modify' && {
        footer: [
            <Button key="delete" type="danger" loading={confirmLoading} onClick={onDelete}>
                Delete
            </Button>,
            <Button key="save" type="primary" loading={confirmLoading} onClick={() => {
                form
                    .validateFields()
                    .then((values) => {
                        form.resetFields();
                        onConfirm(values);
                    })
                    .catch((info) => {
                        console.log('Validate Failed:', info);
                    });
            }}>
                Save
            </Button>
        ]
    };

    const defaultValues = {
        modifier: 'public',
        timeFrame: timeFrame,
        blockLength: blockLength
    };

    useEffect(() => {
        form.setFieldsValue(defaultValues)
    }, [paneToBeModified]);


    const [form] = Form.useForm();
    return (
        <Modal
            visible={visible}
            title={title}
            okText={okText}
            cancelText="Cancel"
            onCancel={onCancel}
            confirmLoading={confirmLoading}
            onOk={() => {
                form
                    .validateFields()
                    .then((values) => {
                        form.resetFields();
                        onConfirm(values);
                    })
                    .catch((info) => {
                        console.log('Validate Failed:', info);
                    });
            }}
            {...deleteProps}
        >
            <Form
                form={form}
                layout="vertical"
                name="form_in_modal"
                initialValues={defaultValues}
            >
                <Form.Item
                    name="timeFrame"
                    label="Time frame of the assessment window"
                    rules={[
                        {
                            required: true,
                            message: 'Please select the time frame of the assessment window!',
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

export default WindowForm;
