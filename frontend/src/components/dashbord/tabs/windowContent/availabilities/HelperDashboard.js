import React, {useContext, useState, useEffect, useRef} from 'react';
import {Table, Input, Button, Popconfirm, Form} from 'antd';
import './HelpersTable.css'
import getDaysArray from "../../../../../utils/datetime";
import AvailChecks from "./AvailChecks";
import {foldSlotData} from "../../../../../utils/dataTransform";

const EditableContext = React.createContext(null);


const EditableRow = ({index, ...props}) => {
    const [form] = Form.useForm();
    return (
        <Form form={form} component={false}>
            <EditableContext.Provider value={form}>
                <tr {...props} />
            </EditableContext.Provider>
        </Form>
    );
};


const EditableCell = ({
                          title,
                          editable,
                          children,
                          dataIndex,
                          record,
                          handleSave,
                          ...restProps
                      }) => {
    const [editing, setEditing] = useState(false);
    const inputRef = useRef(null);
    const form = useContext(EditableContext);
    useEffect(() => {
        if (editing) {
            inputRef.current.focus();
        }
    }, [editing]);

    const toggleEdit = () => {
        setEditing(!editing);
        form.setFieldsValue({
            [dataIndex]: record[dataIndex],
        });
    };

    const save = async () => {
        try {
            const values = await form.validateFields();
            toggleEdit();
            handleSave({...record, ...values});
        } catch (errInfo) {
            console.log('Save failed:', errInfo);
        }
    };

    let childNode = children;

    if (editable) {
        childNode = editing ? (
            <Form.Item
                style={{
                    margin: 0,
                }}
                name={dataIndex}
                rules={[
                    {
                        required: true,
                        message: `${title} is required.`,
                    },
                ]}
            >
                <Input ref={inputRef} onPressEnter={save} onBlur={save}/>
            </Form.Item>
        ) : (
            <div
                className="editable-cell-value-wrap"
                style={{
                    paddingRight: 24,
                }}
                onClick={toggleEdit}
            >
                {children}
            </div>
        );
    }

    return <td {...restProps}>{childNode}</td>;
};


const HelpersTable = ({window}) => {
    const slotData = foldSlotData(window.block_slots);
    const days = getDaysArray(window.start_date, window.end_date);
    const columnInfo = [
        {
            title: 'Email',
            dataIndex: 'email',
            width: '25%',
            editable: true,
        },
        ...days.map(day => (
            {
                title: day,
                dataIndex: day,
                key: day,
            }
        )),
        {
            title: 'operation',
            dataIndex: 'operation',
            render: (_, record) =>
                dataSource.length >= 1 ? (
                    <Popconfirm title="Sure to delete?" onConfirm={() => handleDelete(record.key)}>
                        <a>Delete</a>
                    </Popconfirm>
                ) : null,
        },
    ];

    const [count, setCount] = useState(0);
    const [dataSource, setDataSource] = useState([]);
    const [availData, setAvailData] = useState({});

    const handleDelete = (key) => {
        setDataSource(dataSource.filter((item) => item.key !== key));
    };
    const handleAdd = () => {
        let dayElements = days.map(day => (
            {
                [day]: <AvailChecks
                    key={day}
                    day={day}
                    assessor='@code.berlin'
                    availableTimes={slotData[day]}
                    availData={availData}
                    setAvailData={setAvailData}
                />
            }
        ));

        const newData = Object.assign(
            {
                key: count,
                email: '@code.berlin',
            },
            ...dayElements
        );

        setDataSource([...dataSource, newData]);
        setCount(count + 1);
    };
    const handleSave = (row) => {
        const index = dataSource.findIndex((item) => row.key === item.key);
        const item = dataSource[index];
        dataSource.splice(index, 1, {...item, ...row});
        setDataSource([...dataSource])
    };

    const components = {
        body: {
            row: EditableRow,
            cell: EditableCell,
        },
    };
    const columns = columnInfo.map((col) => {
        if (!col.editable) {
            return col;
        }

        return {
            ...col,
            onCell: (record) => ({
                record,
                editable: col.editable,
                dataIndex: col.dataIndex,
                title: col.title,
                handleSave: handleSave,
            }),
        };
    });

    return (
        <div>
            <Button
                onClick={handleAdd}
                type="primary"
                shape="round"
                style={{
                    marginBottom: "30px",
                    marginLeft: "20px",
                    float: "left"
                }}
            >
                Add a row
            </Button>
            <Table
                components={components}
                rowClassName={() => 'editable-row'}
                bordered
                dataSource={dataSource}
                columns={columns}
                tableLayout={"fixed"}
            />
        </div>
    );
};

export default HelpersTable;
