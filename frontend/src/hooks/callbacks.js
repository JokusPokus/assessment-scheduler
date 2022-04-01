import { httpGetPhases } from "./requests"

const getFormattedPhases = async () => {
    const fetchedPhases = await httpGetPhases();
    return fetchedPhases.reduce((r, a) => {
        r[a.year] = r[a.year] || [];
        r[a.year].push(a.semester);
        return r;
    }, Object.create(null));
};

export default getFormattedPhases;
