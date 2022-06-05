import React, {useEffect, useState, createRef} from 'react';
import getDaysArray from "../../../../../utils/datetime";
import {Button, Input, message, Popconfirm, Table, Tooltip} from "antd";
import {httpGetStaff, httpPostStaffAvails, httpDeleteHelper} from "../../../../../hooks/requests";
import {foldSlotData, foldStaffData} from "../../../../../utils/dataTransform";
import {UserAddOutlined, DeleteOutlined} from "@ant-design/icons";
import AvailChecks from "./AvailChecks";
import {NextStepButton, SaveButton} from "../Buttons";


const StaffTable = ({window, windowStep, setWindowStep, apiResourceName, extensible, setPhaseData}) => {
    const emailColumn = [
        {
            title: 'Email',
            dataIndex: 'email',
            key: 'email',
            width: '25%',
        },
    ];
    let [newEmail, setNewEmail] = useState('');

    const days = getDaysArray(window.start_date, window.end_date);
    const daysColumns = days.map(day => (
        {
            title: day,
            dataIndex: day,
            key: day,
        }
    ));

    const processStatus = {
        INITIAL: "initial",
        LOADING: "loading",
        SUCCESS: "success",
        FAILURE: "failure"
    };

    const [staff, setStaff] = useState([]);
    const [availData, setAvailData] = useState({});
    const [status, setStatus] = useState(processStatus.INITIAL);
    const [saveButtonDisabled, setSaveButtonDisabled] = useState(true);
    const [dataSource, setDataSource] = useState([]);

    const slotData = foldSlotData(window.block_slots);

    const getStaff = async () => {
        const response = await httpGetStaff(window.id, apiResourceName)();
        let staffData = await response.json();
        staffData = staffData.map(person => (
            {
                ...person,
                available_blocks: person.available_blocks.filter(
                    block => block.window === window.id
                )
            }
        ));
        setStaff(staffData);
    };

    useEffect(async () => {
        await getStaff();
    }, []);

    useEffect(() => {
        setAvailData(foldStaffData(staff));
    }, [staff]);

    useEffect(() => {
        // Are all the availabilities empty?
        const mustDisable = Object.values(availData).map(obj => (
                Object.values(obj).every(x => x.length === 0)
            )
        ).every(Boolean);
        setSaveButtonDisabled(mustDisable);
    }, [availData]);

    useEffect(() => {
        const staffTableSource = Object.keys(availData).length > 0
            ? Object.keys(availData).map(email => {
                let dayElements = days.map(day => (
                    {
                        [day]: <AvailChecks
                            key={day}
                            day={day}
                            staff={email}
                            availableTimes={slotData[day]}
                            availData={availData}
                            setAvailData={setAvailData}
                        />
                    }
                ));
                return Object.assign(
                    {
                        email: email,
                        key: email
                    },
                    ...dayElements
                )
            })
            : [];
        setDataSource([...staffTableSource]);
    }, [availData]);

    const handleDelete = async (key) => {
        setDataSource(dataSource.filter((item) => item.key !== key));
        const response = await httpDeleteHelper(key, window.id)();
        if (response.status === 200) {
            message.success(`Helper ${key} successfully deleted`);
        } else {
            message.error("Something went wrong...");
        }
    };

    const handleEmailChange = (e) => {
        setNewEmail(e.target.value)
    };

    const handleAdd = () => {
        const email = `${newEmail}@code.berlin`;
        let dayElements = days.map(day => (
            {
                [day]: <AvailChecks
                    key={day}
                    day={day}
                    staff={email}
                    availableTimes={slotData[day]}
                    availData={availData}
                    setAvailData={setAvailData}
                />
            }
        ));

        const newData = Object.assign(
            {
                key: email,
                email: email
            },
            ...dayElements
        );

        setNewEmail('');
        availData[email] = {};
        setAvailData(availData);
        setDataSource([...dataSource, newData]);
    };

    const saveAvails = async () => {
        setStatus(processStatus.LOADING);

        const response = await httpPostStaffAvails(window.id, availData, apiResourceName)();
        if (response.status === 200) {
            message.success(`You successfully saved ${apiResourceName} availabilities.`);
            setStatus(processStatus.SUCCESS);
            await getStaff();
            await setPhaseData();
        } else {
            message.error("Something went wrong...");
            setStatus(processStatus.FAILURE);
        }
    };

    let columns = [...emailColumn, ...daysColumns];

    if (extensible) {
        columns.push({
            title: '',
            dataIndex: 'delete',
            width: '5em',
            align: 'center',
            render: (_, record) =>
                dataSource.length >= 1 ? (
                    <Popconfirm
                        title="Sure to delete? This will remove the helper from the entire assessment phase."
                        onConfirm={() => handleDelete(record.key)}
                        placement={"topRight"}
                    >
                        <a><DeleteOutlined style={{fontSize: "1.5em"}}/></a>
                    </Popconfirm>
                ) : null,
        });
    }

    return (
        <div className='fade-in' style={{marginTop: "60px"}}>
            <Table
                bordered
                dataSource={dataSource}
                columns={columns}
                tableLayout={"fixed"}
                pagination={false}
            />
            <div style={{display: extensible && "flex", width: "100%"}}>
                {extensible &&
                <Input.Group
                    compact
                    style={{
                        marginTop: "30px",
                        marginRight: "20px",
                    }}
                >
                    <Input
                        style={{width: '20vw', textAlign: 'right', float: "left"}}
                        onChange={handleEmailChange}
                        onPressEnter={handleAdd}
                        suffix="@code.berlin"
                        value={newEmail}
                    />
                    <Button
                        type="primary"
                        shape="round"
                        style={{float: "left"}}
                        onClick={handleAdd}
                        icon={<UserAddOutlined/>}
                    />

                </Input.Group>
                }
                <Tooltip title={saveButtonDisabled ? "Please add/select start times" : undefined}>
                    <SaveButton
                        status={status}
                        disabled={saveButtonDisabled}
                        title="Save availabilities"
                        onClick={saveAvails}
                    />
                </Tooltip>
                <NextStepButton
                    windowStep={windowStep}
                    setWindowStep={setWindowStep}
                    status={status}
                />
            </div>

        </div>
    )
};

export default StaffTable;
