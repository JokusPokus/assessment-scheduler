import React from 'react';
import {Empty, Button} from "antd";

const WindowAdder = ({currentPhase}) => {
    return (
        <Empty description={<span>No weeks yet...</span>}>
            <Button type="primary">Add first week</Button>
        </Empty>
    );
};

export default WindowAdder;
