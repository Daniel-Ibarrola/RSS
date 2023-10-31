import {useEffect, useReducer} from "react";
import Card from "react-bootstrap/Card";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Image from "react-bootstrap/Image";
import Row from "react-bootstrap/Row";

import { Map } from "../Map/index.js";
import {
    FailFetch,
    LoadSpinner,
    lastAlertURL,
    fetchDataReducer,
    fetchData, alertsURL,
} from "../shared/index.js";
import { getTitle }  from "./utils.js";
import "./style.css";




const AlertBody = ({ data }) => {
    return (
        <>
            <p className="feed-content-title">{getTitle(data.states, data.region, data.time, data.is_event)}</p>
            <p><strong>Severidad</strong>: {data.is_event ? "Menor": "Mayor"}</p>
            <Map
                className={"align-self-center"}
                isEvent={data.is_event}
                region={data.region}
                states={data.states}
            />
         </>
    );
}

const Feed = () => {
    const [lastAlert, dispatchLastAlert] = useReducer(
        fetchDataReducer,
        {
            data: {},
            isLoading: false,
            isError: false
        }
    );

    useEffect(() => {
        fetchData(dispatchLastAlert, lastAlertURL);
    }, []);

    return (
        <Container className="feed">
            <Row className="justify-content-center">
                <Col md={{span: 6}}>
                    <Card>
                        <Card.Header className="feed-title">
                                <Image
                                    alt="sasmex-rss logo"
                                    src="ciresFeedLogo2b.png"
                                />
                            <strong> <a href={alertsURL + "latest/cap/"}>Último CAP</a></strong>
                        </Card.Header>
                        <Card.Body>
                            {lastAlert.isError && <FailFetch />}
                            {lastAlert.isLoading && <LoadSpinner />}
                            {Object.keys(lastAlert.data).length > 0 && <AlertBody data={lastAlert.data} />}
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
    );
};


export { AlertBody, Feed };