import React from 'react';
import WindowSteps from "./WindowSteps";

const WindowContent = ({window}) => {
    return(
        <WindowSteps
            style={{ paddingTop: "100px" }}
            window={window}
        />
    );
};

export default WindowContent;
