import React, {useEffect, useState} from 'react';
import {Upload, Form, Button, Result} from 'antd';
import {InboxOutlined} from '@ant-design/icons';
import {httpPostPlanningSheet} from "../../../../../hooks/requests";
import {UploadError, UploadSuccess} from "./UploadFeedback";
import UploadForm from "./UploadForm";
import "../WindowSteps.css"

const {Dragger} = Upload;
const _ = require('lodash');

const CSVDashboard = ({
                          window,
                          windowStep,
                          setWindowStep,
                          uploadSuccess,
                          setUploadSuccess,
                          uploadErrors,
                          setUploadErrors
                      }) => {

    const [isUploading, setIsUploading] = useState(false);
    const [displaySuccess, setDisplaySuccess] = useState(false);

    useEffect(() => {
        if (!_.isEmpty(window)) {
            setDisplaySuccess(window.csv_uploaded)
        }
    }, [window]);

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
                if ('csv' in body) {
                    let newErrors = {};
                    if ('missing_cols' in body.csv) {
                        newErrors.missingCols = body.csv.missing_cols;
                    }
                    if ('wrong_email_format' in body.csv) {
                        newErrors.wrongEmailCols = body.csv.wrong_email_format;
                    }
                    setUploadErrors({...uploadErrors, ...newErrors});
                }
            }
            setIsUploading(false);
        }, 1000);

    };

    return (
        <>
            {uploadSuccess || displaySuccess ? (
                <UploadSuccess
                    windowStep={windowStep}
                    setWindowStep={setWindowStep}
                    setDisplaySuccess={setDisplaySuccess}
                    setUploadSuccess={setUploadSuccess}
                />
            ) : !_.isEmpty(uploadErrors) ? (
                <div style={{maxWidth: '50%', margin: 'auto'}}>
                    <UploadError
                        uploadErrors={uploadErrors}
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