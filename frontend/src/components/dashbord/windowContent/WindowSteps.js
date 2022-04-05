import React, {useState} from 'react';
import {Steps, Button, message} from 'antd';
import './WindowSteps.css'

const {Step} = Steps;

const WindowSteps = () => {
    const [current, setCurrent] = useState(0);

    const steps = [
        {
            title: 'First',
            content: 'First-content',
        },
        {
            title: 'Second',
            content: 'Second-content',
        },
        {
            title: 'Last',
            content: 'Last-content',
        },
    ];

    const onChange = newStep => {
        setCurrent(newStep);
    };

    return (
        <div style={{marginTop: "20px"}}>
            <Steps current={current} onChange={onChange}>
                {steps.map(item => (
                    <Step key={item.title} title={item.title}/>
                ))}
            </Steps>
            <div className="steps-content">{steps[current].content}</div>
            <div className="steps-action">
                {current < steps.length - 1 && (
                    <Button type="primary">
                        Next
                    </Button>
                )}
                {current === steps.length - 1 && (
                    <Button type="primary" onClick={() => message.success('Processing complete!')}>
                        Done
                    </Button>
                )}
                {current > 0 && (
                    <Button style={{margin: '0 8px'}}>
                        Previous
                    </Button>
                )}
            </div>

        </div>
    );
};

export default WindowSteps;
