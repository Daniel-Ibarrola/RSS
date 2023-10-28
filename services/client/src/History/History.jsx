import {useEffect, useReducer} from "react";
import Accordion from 'react-bootstrap/Accordion';
import Button from 'react-bootstrap/Button';
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import DatePicker from "react-datepicker";
import Form from "react-bootstrap/Form";
import Pagination from 'react-bootstrap/Pagination';
import Table from 'react-bootstrap/Table';
import {AlertTypes, getValidFilters, removeAccents} from "./filters.js";
import { historyReducer, HISTORY_ACTIONS } from "./historyReducer.js";
import {
    alertsURL,
    fetchData,
    FailFetch,
    LoadSpinner,
    REGIONS,
    STATES,
    STATE_CODES
} from "../shared/index.js";

import "./style.css";
import "react-datepicker/dist/react-datepicker.css";


const getType = (isEvent, numRefs) => {
    let type = "";
    if (isEvent){
        type = "Evento";
    } else{
        type = "Alerta";
    }

    if (numRefs > 0){
        type += " / Actualización";
    }
    return type;
};

const getStates = (states) => {
    return  states.map(c => STATES[c]).join(", ");
}

const AlertsTable = ({ alerts }) => {
    // TODO: remove T from date. Example: 2023-09-14T00:00:00
    return (
        <Table striped bordered hover>
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>Estado(s)</th>
                    <th>Región</th>
                    <th>Tipo</th>
                    <th>Archivo</th>
                </tr>
            </thead>
            <tbody>
            {alerts.map(item => (
                <tr key={item.id}>
                    <td>{item.time.split("T").join(" ")}</td>
                    <td>{getStates(item.states)}</td>
                    <td>{REGIONS[item.region]}</td>
                    <td>{getType(item.is_event, item.references.length)}</td>
                    <td>
                        <a href={alertsURL + item.id + "/cap/?save=true"}>{item.id + ".cap"}</a>
                    </td>
                </tr>
            ))}
            </tbody>
        </Table>
    );
};


const FilterFormSelect = ({title, options, onChange}) => {
    return (
            <Form.Group as={Col}>
                <Form.Label>{title}</Form.Label>
                <Form.Select onChange={onChange}>
                    <option>-</option>
                    {options.map(op => <option key={op} value={op}>{op}</option>)}
                </Form.Select>
            </Form.Group>
    );
}

const FiltersForm = (props) => {
    return (
        <Form onSubmit={props.onSubmit} className="filters-form">
            <h2>Filtros</h2>
            <Row className="form-selectors">
                <FilterFormSelect
                    title="Tipo"
                    options={["Todos", "Alerta", "Evento"]}
                    onChange={props.onTypeChange}
                />
                <FilterFormSelect
                    title="Estado"
                    options={Object.values(STATES)}
                    onChange={props.onStateChange}
                />
                <FilterFormSelect
                    title="Región"
                    options={[...new Set(Object.values(REGIONS))].sort()}
                    onChange={props.onRegionChange}
                />
            </Row>
            <Row className="date-pickers" xs={3}>
                <Form.Group as={Col}>
                    <Row>
                        <Form.Label>Fecha Inicio</Form.Label>
                    </Row>
                    <Row>
                        <DatePicker
                            showIcon
                            selected={props.startDate}
                            onChange={props.onStartChange}
                            placeholderText="Fecha inicial"
                            classname=".date-picker"
                        />
                    </Row>
                </Form.Group>
                <Form.Group as={Col}>
                    <Row>
                        <Form.Label>Fecha Fin</Form.Label>
                    </Row>
                    <Row>
                        <DatePicker
                            showIcon
                            selected={props.endDate}
                            onChange={props.onEndChange}
                            placeholderText="Fecha final"
                            classname=".date-picker"
                        />
                    </Row>
                </Form.Group>
            </Row>
            <Button type="submit">Aplicar</Button>
        </Form>
    )
};


const HistoryPagination = ({ activePage, numPages, onPageClick }) => {
    const pages = [...Array(numPages).keys()];
    return (
        <Pagination>
            {pages.map(pg => (
                <Pagination.Item
                    active={pg + 1 === activePage}
                    key={pg + 1}
                    onClick={() => onPageClick(pg + 1)}
                >
                    {pg + 1}
                </Pagination.Item>)
            )}
        </Pagination>
    );
};


const HistoryData = () => {
    const [alerts, dispatchAlerts] = useReducer(
        historyReducer,
        {
            data: {},
            page: 1,
            startDate: null,
            endDate: null,
            isLoading: false,
            isError: false,
            type: AlertTypes.Todos,
            state: null,
            region: null,
        }
    );

    useEffect(() => {
        const filters = getValidFilters(alerts);
        fetchData(dispatchAlerts, alertsURL, HISTORY_ACTIONS, filters);
    }, [alerts.page]);

    const handlePageChange = (newPage) => {
        dispatchAlerts({
            type: HISTORY_ACTIONS.SET_PAGE,
            payload: newPage
        });
    };

    const handleTypeChange = (event) => {
        if (event.target.value === "-"){
            dispatchAlerts({
                type: HISTORY_ACTIONS.SET_TYPE,
                payload: null
            })
        } else {
            dispatchAlerts({
                type: HISTORY_ACTIONS.SET_TYPE,
                payload: AlertTypes[event.target.value]
            });
        }
    };

    const handleStateChange = (event) => {
        if (event.target.value === "-"){
            dispatchAlerts({
                type: HISTORY_ACTIONS.SET_STATE,
                payload: null
            })
        } else {
            const state = STATE_CODES[removeAccents(event.target.value)];
            dispatchAlerts({
                type: HISTORY_ACTIONS.SET_STATE,
                payload: state
            });
        }
    };

    const handleRegionChange = (event) => {
        if (event.target.value === "-"){
            dispatchAlerts({
                type: HISTORY_ACTIONS.SET_REGION,
                payload: null
            });
        } else {
            dispatchAlerts({
                type: HISTORY_ACTIONS.SET_REGION,
                payload: event.target.value.replace(/\s+/g, '').toLowerCase()
            });
        }
    };

    const handleStartDateChange = (newDate) => {
        dispatchAlerts({
            type: HISTORY_ACTIONS.SET_START,
            payload: newDate,
        });
    };

    const handleEndDateChange = (newDate) => {
        dispatchAlerts({
            type: HISTORY_ACTIONS.SET_END,
            payload: newDate,
        });
    };

    const handleApplyFilters = async (event) => {
        event.preventDefault();
        const filters = getValidFilters(alerts);
        await fetchData(dispatchAlerts, alertsURL, HISTORY_ACTIONS, filters);
    }

    return (
        <Container>
            <Row>
                <FiltersForm
                    startDate={alerts.startDate}
                    endDate={alerts.endDate}
                    onTypeChange={handleTypeChange}
                    onStateChange={handleStateChange}
                    onRegionChange={handleRegionChange}
                    onStartChange={handleStartDateChange}
                    onEndChange={handleEndDateChange}
                    onSubmit={handleApplyFilters}
                />
            </Row>
            <Row>
                {alerts.isLoading && <LoadSpinner />}
                {alerts.isError && <FailFetch />}
                {Object.keys(alerts.data).length > 0 &&
                    <>
                        <AlertsTable alerts={alerts.data.alerts}/>
                        <HistoryPagination
                            activePage={alerts.page}
                            numPages={Math.ceil(alerts.data.count / 20)}
                            onPageClick={handlePageChange}
                        />
                    </>
                }
            </Row>
        </Container>
    );
};


const History = () => {

    return (
        <Accordion className="history-accordion">
            <Accordion.Item eventKey={"0"}>
                <Accordion.Header>Historial de Alertas (CAP)</Accordion.Header>
                <Accordion.Body>
                   <HistoryData />
                </Accordion.Body>
            </Accordion.Item>
        </Accordion>
    );
};

export { History, HistoryData };
