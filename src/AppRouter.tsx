import React from "react";
import { HashRouter, Route, Routes } from "react-router-dom";
import App from "./App.tsx";
import Faq from "./components/Faq.tsx";
import logo from './assets/logo.svg';
import HowTo from "./components/HowTo.tsx";

function AppRouter() {
    return (
        <div>
            <nav className="navbar navbar-expand-lg navbar-light">
                <img src={logo} className="navbar-brand d-inline-block align-top mx-3" alt="CDS logo" />
                <a className="navbar-brand text-primary" href="/EPND-FAIRification">FAIRNotator</a>
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav mr-auto">
                        <li className="nav-item active">
                            <a className="nav-link text-primary" href="https://github.com/MaastrichtU-CDS/EPND-FAIRification">GitHub</a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link text-primary" href="/EPND-FAIRification/howto">How-to</a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link text-primary" href="/EPND-FAIRification/faq">FAQ</a>
                        </li>
                    </ul>
                </div>
            </nav>
            <HashRouter>
                <Routes>
                    <Route path="/EPND-FAIRification" element={<App />} />
                    <Route path="/EPND-FAIRification/faq" element={<Faq />} />
                    <Route path="/EPND-FAIRification/howto" element={<HowTo />} />
                </Routes>
            </HashRouter>
        </div>
    )
}

export default AppRouter;