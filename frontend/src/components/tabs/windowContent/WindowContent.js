import React from 'react';
import WindowSteps from "./WindowSteps";

const WindowContent = ({window, setPhaseData}) => {
    return(
        <WindowSteps
            style={{ paddingTop: "100px" }}
            window={window}
            setPhaseData={setPhaseData}
        />
    );
};

export default WindowContent;
