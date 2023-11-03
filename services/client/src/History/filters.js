

export const AlertTypes = {
    Todos: "all",
    Alerta: "alert",
    Evento: "event"
};


export const removeAccents = (str) => {
    return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
};


export const getValidFilters = (filters) => {
    const valid = {};
    if (filters.page){
        valid.page = filters.page;
    }
    if (filters.type){
        valid.type = filters.type;
    }
    if (filters.state){
        valid.state = filters.state;
    }
    if (filters.region) {
        valid.region = filters.region;
    }
    if (filters.startDate){
        valid.start_date = filters.startDate.toISOString().split("T")[0];
    }
    if (filters.endDate){
        valid.end_date = filters.endDate.toISOString().split("T")[0];
    }
    return valid;
};
