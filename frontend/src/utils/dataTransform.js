export const foldSlotData = (slots) => (
    slots.reduce((r, a) => {
        r[a.date] = r[a.date] || [];
        r[a.date].push(a.time);
        return r;
    }, Object.create(null))
);


export const foldAssessorData = (assessors) => (
    assessors.reduce((r, a) => {
        r[a.email] = r[a.email] || {};
        r[a.email] = a['available_blocks'].reduce((rr, aa) => {
            rr[aa.date] = rr[aa.date] || [];
            rr[aa.date].push(aa.time);
            return rr
        }, {});
        return r;
    }, {})
);
