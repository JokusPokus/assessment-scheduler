export const foldSlotData = (slots) => (
    slots.reduce((r, a) => {
        r[a.date] = r[a.date] || [];
        r[a.date].push(a.time);
        return r;
    }, Object.create(null))
);
