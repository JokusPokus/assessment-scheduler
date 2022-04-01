import { useCallback, useEffect, useState } from "react"
import { httpGetPhases } from "./requests"

const usePhases = ( didAddPhase ) => {
    const [phases, setPhases] = useState([]);

    useEffect(() => {
        const getPhases = async () => {

            const fetchedPhases = await httpGetPhases();

            const formattedPhases = fetchedPhases.reduce((r, a) => {
                r[a.year] = r[a.year] || [];
                r[a.year].push(a.semester);
                return r;
            }, Object.create(null));

            setPhases(formattedPhases);
        };
        getPhases()
    }, [didAddPhase]);

    return phases
};

export default usePhases;
