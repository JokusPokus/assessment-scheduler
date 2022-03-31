import { useCallback, useEffect, useState } from "react"
import { httpGetPhases } from "./requests"

const usePhases = () => {
    const [phases, setPhases] = useState([]);

    const getPhases = useCallback(async () => {
        const fetchedPhases = await httpGetPhases();

        const formattedPhases = fetchedPhases.reduce((r, a) => {
            r[a.year] = r[a.year] || [];
            r[a.year].push(a.semester);
            return r;
        }, Object.create(null));

        setPhases(formattedPhases);
    }, []);

    useEffect(() => {
        getPhases()
    }, [getPhases]);

    return phases
};

export default usePhases;
