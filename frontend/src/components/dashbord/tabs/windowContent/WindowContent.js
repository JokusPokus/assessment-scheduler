import React from 'react';
import WindowSteps from "./WindowSteps";

const WindowContent = ({phase, window, setPhaseData}) => {
    return(
        <WindowSteps
            style={{ paddingTop: "100px" }}
            phase={phase}
            window={window}
            setPhaseData={setPhaseData}
        />
    );
};

export default WindowContent;
