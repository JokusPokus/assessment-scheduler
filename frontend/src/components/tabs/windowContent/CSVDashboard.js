import React, {useState} from 'react';
import {Upload, Form, Button, Result} from 'antd';
import {InboxOutlined} from '@ant-design/icons';
import {httpPostPlanningSheet} from "../../../hooks/requests";
import {UploadError, UploadSuccess} from "./UploadFeedback";
import UploadForm from "./UploadForm";
import "./WindowSteps.css"

const {Dragger} = Upload;

const CSVDashboard = ({
                          window,
                          windowStep,
                          setWindowStep,
                          uploadSuccess,
                          setUploadSuccess,
                          missingColumns,
                          setMissingColumns
                      }) => {

    const [isUploading, setIsUploading] = useState(false);

    const onFinish = async (values) => {
        setIsUploading(true);
        const response = await httpPostPlanningSheet(
            {
                csv: values.planningSheet[0].originFileObj,
                window: window.id
            }
        );
        setTimeout(async () => {
            if (response.status === 200) {
                setUploadSuccess(true);
            } else if (response.status === 400) {
                const body = await response.json();
                if ('csv' in body && 'missing_cols' in body.csv) {
                    setMissingColumns(body.csv.missing_cols);
                }
            }
            setIsUploading(false);
        }, 1000);

    };

    return (
        <>
            {uploadSuccess ? (
                <UploadSuccess windowStep={windowStep} setWindowStep={setWindowStep}/>
            ) : missingColumns.length > 0 ? (
                <div style={{maxWidth: '50%', margin: 'auto'}}>
                    <UploadError
                        missingColumns={missingColumns}
                    />
                    <UploadForm
                        onFinish={onFinish}
                        isUploading={isUploading}
                        style={{width: '100%'}}
                    />
                </div>
            ) : (
                <div style={{maxWidth: '50%', margin: '64px auto'}}>
                    <UploadForm
                        style={{maxWidth: '50%'}}
                        onFinish={onFinish}
                        isUploading={isUploading}
                    />
                </div>
            )}
        </>
    );
};

export default CSVDashboard;