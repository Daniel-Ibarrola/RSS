import Container from "react-bootstrap/Container";
import RBNavbar from "react-bootstrap/Navbar";
import Row from "react-bootstrap/Row";

import { Feed } from "./Feed/index.js";
import { History } from "./History/index.js";
import './App.css'

const NavBar = () => {
    return (
        <RBNavbar bg="dark">
            <Container>
                <RBNavbar.Brand className="navbar">
                    <img
                        alt=""
                        src="cires.png"
                        width="50"
                        height="50"
                        className="d-inline-block align-top"
                    /> <h1>SASMEX CAP</h1>
                </RBNavbar.Brand>
            </Container>
        </RBNavbar>
    );
};


const App = () => {
  return (
    <>
        <NavBar />
        <Container>
            <Row>
                <Feed />
            </Row>
           <Row>
               <History />
           </Row>
        </Container>
    </>
  );
};

export default App;
