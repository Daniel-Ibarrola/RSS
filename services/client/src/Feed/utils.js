import { STATES, REGIONS } from "../shared/index.js";


export const getTitle = (states, region, time, isEvent=false) => {
    const date = new Date(time);
    let dateStr = date.toLocaleDateString("es-MX", {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: "numeric",
        minute: "numeric",
        second: "numeric",
        hour12: false
    });
    dateStr = dateStr.charAt(0).toUpperCase() + dateStr.slice(1);
    const statesStr = states.map(c => STATES[c]).join("/");

    if (isEvent){
        return  `${dateStr} Sismo en ${REGIONS[region]}.`;
    }
    return `${dateStr} Alerta en ${statesStr} por sismo en ${REGIONS[region]}.`;

};
