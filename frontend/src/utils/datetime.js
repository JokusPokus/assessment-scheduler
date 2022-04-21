const getDaysArray = (start, end) => {
    let arr = [];
    for(let dt=new Date(start); dt <= new Date(end); dt.setDate(dt.getDate() + 1)){
        arr.push(new Date(dt).toISOString().split('T')[0]);
    }
    return arr;
};

export default getDaysArray;
