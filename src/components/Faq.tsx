import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Accordion from 'react-bootstrap/Accordion';

const Faq = () => {
    return (
        <div className="container mt-5">
            <h1 className="mb-4">Frequently Asked Questions (FAQ)</h1>
            <Accordion defaultActiveKey="0">
                <Accordion.Item eventKey="0">
                    <Accordion.Header>
                        Why should I use the FAIRNotator?
                    </Accordion.Header>
                    <Accordion.Body>
                        While there are many different possible output forms and formats for a FAIRification process, the initial need to map local data syntax to a common standard is a universal requirement. The FAIRNotator is designed as a user-friendly tool that allows non-technical domain experts to map their data to a common standard. The JSON-LD output can then be used as an input for further ETL transformations based on your project's needs. 
                    </Accordion.Body>
                </Accordion.Item>
                <Accordion.Item eventKey="1">
                    <Accordion.Header>
                        What is the current status of the application?
                    </Accordion.Header>
                    <Accordion.Body>
                        The FAIRNotator is still in the development phase. The current version assumes a hardcoded version of the terminology sheet for example.
                    </Accordion.Body>
                </Accordion.Item>
                <Accordion.Item eventKey="2">
                    <Accordion.Header>
                        Can I perform mappings on multiple CSVs or a database?
                    </Accordion.Header>
                    <Accordion.Body>
                        The FAIRNotator currently only supports uploading a single CSV, or adding data manually. 
                    </Accordion.Body>
                </Accordion.Item>
                <Accordion.Item eventKey="3">
                    <Accordion.Header>
                        How does the FAIRNotator handle privacy sensitive data?
                    </Accordion.Header>
                    <Accordion.Body>
                        The FAIRNotator is a client-side application, which means the data you provide never leaves your device. The JSON-LD output of the FAIRNotator contains only mappings to the syntactical structure of your data, and does not contain any of the potentially privacy sensitive data itself.
                    </Accordion.Body>
                </Accordion.Item>
            </Accordion>
        </div>
    );
};

export default Faq;