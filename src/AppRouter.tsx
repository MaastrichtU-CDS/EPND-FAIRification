import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
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
                            <a className="nav-link text-primary" href="/howto">How-to</a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link text-primary" href="/faq">FAQ</a>
                        </li>
                    </ul>
                </div>
            </nav>
            <BrowserRouter>
                <Routes>
                    <Route path="/EPND-FAIRification" element={<App />} />
                    <Route path="/faq" element={<Faq />} />
                    <Route path="/howto" element={<HowTo />} />
                </Routes>
            </BrowserRouter>
        </div>
    )
}

export default AppRouter;