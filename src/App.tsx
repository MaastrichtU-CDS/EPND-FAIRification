import React, { useEffect, useState } from 'react';
import CsvUploader from './components/CsvUploader.tsx';
import GoogleSheetReader from './components/GoogleSheetReader.tsx';
import CategoricalValues from './components/CategoricalValues.tsx';
import { mean, std, min, max } from 'mathjs';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.scss';
import JsonLdService from './services/JsonLdService.js';
import { OntologyTerm } from './models/ontology-term.ts';
import { ValueMapping } from './models/value-mapping.ts';
import logo from './assets/logo.svg';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

function App() {
  const [googleSheetData, setGoogleSheetData] = useState([]);
  const [localTerms, setLocalTerms] = useState([]);
  const [selectedOntologyTerm, setSelectedOntologyTerm] = useState<OntologyTerm | null>(null);
  const [showList, setShowList] = useState(false);
  const [selectedMapping, setSelectedMapping] = useState('');
  const [csvData, setCsvData] = useState([]);
  const [csvFileName, setCsvFileName] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    JsonLdService.initDB();
  }, []);


  const handleGoogleSheetData = (data: any) => {
    setGoogleSheetData(data);
    setShowList(true);
  };

  const handleCsvUpload = (localTerms: any, data: any, fileName: string) => {
    setLocalTerms(localTerms);
    setCsvData(data);
    setCsvFileName(fileName);
  };

  const handleOntologyTermClick = (ontologyTerm: OntologyTerm) => {
    setSelectedOntologyTerm(ontologyTerm);
    JsonLdService.getMapping(ontologyTerm.ontologyClass).then((mapping) => {
      if (!mapping || !mapping.source || !mapping.source.column) {
        setSelectedMapping('');
      } else {
        setSelectedMapping(mapping.source.column);
      }
    });
  };

  const handleSheetCloseClick = () => {
    setShowList(false);
    setSelectedOntologyTerm(null);
  };

  const handleMappingChange = (event: any) => {
    if (!selectedOntologyTerm) return;
    const selectedLocalTerm = event.target.value;
    if (selectedLocalTerm == null || undefined) return;
    setSelectedMapping(selectedLocalTerm);
    const fileNameWithoutExtension = csvFileName.replace(/\.[^/.]+$/, "");
    JsonLdService.addCsvDatasource(fileNameWithoutExtension, localTerms).then(() => {
      if (selectedLocalTerm === "") {
        JsonLdService.deleteMapping({
          uri: selectedOntologyTerm.ontologyClass,
        });
      } else {
        JsonLdService.addMapping(
          {
            database: fileNameWithoutExtension,
            table: fileNameWithoutExtension,
            column: selectedLocalTerm,
          },
          {
            type: selectedOntologyTerm.unit,
            uri: selectedOntologyTerm.ontologyClass,
            name: selectedOntologyTerm.variable,
          }
        );
      }
    });
  };

  const getColumnStatistics = (column) => {
    const columnData = csvData.map((row) => parseFloat(row[column])).filter((value) => !isNaN(value));
    if (!columnData || columnData.length === 0) {
      return {
        mean: 0,
        std: 0,
        count: 0,
        min: 0,
        max: 0,
      };
    }
    return {
      mean: mean(columnData),
      std: std(columnData),
      count: columnData.length,
      min: min(columnData),
      max: max(columnData),
    };
  };

  const handleExportJsonLd = async () => {
    const jsonLdObject = await JsonLdService.getJsonLdObject();
    const blob = new Blob([JSON.stringify(jsonLdObject, null, 2)], { type: 'application/json' });

    // Remove file extension
    const fileNameWithoutExtension = csvFileName.replace(/\.[^/.]+$/, "");

    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${fileNameWithoutExtension}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const deleteJsonLd = async () => {
    setIsModalOpen(false);
    await JsonLdService.deleteJsonLdObject();
    if (!selectedOntologyTerm) return;
    handleOntologyTermClick(selectedOntologyTerm);
  }

  const toggleModal = () => {
    setIsModalOpen(!isModalOpen);
  };

  return (
    <div>
      <Modal show={isModalOpen} onHide={toggleModal}>
        <Modal.Header closeButton>
          <Modal.Title>Warning</Modal.Title>
        </Modal.Header>
        <Modal.Body>All mapping data will be deleted. Are you sure?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={toggleModal}>Cancel</Button>
          <Button variant="danger" onClick={deleteJsonLd}>Yes</Button>
        </Modal.Footer>
      </Modal>
      <nav className="navbar navbar-expand-lg navbar-light">
        <img src={logo} className="navbar-brand d-inline-block align-top mx-3" />
        <a className="navbar-brand text-primary" href="#">FAIRnotator</a>
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav mr-auto">
            <li className="nav-item active">
              <a className="nav-link text-primary" href="https://github.com/MaastrichtU-CDS/EPND-FAIRification">GitHub</a>
            </li>
            <li className="nav-item">
              <a className="nav-link text-primary" href="https://github.com/MaastrichtU-CDS/EPND-FAIRification">How-to</a>
            </li>
            <li className="nav-item">
              <a className="nav-link text-primary" href="https://github.com/MaastrichtU-CDS/EPND-FAIRification">FAQ</a>
            </li>
          </ul>
        </div>
        <button className="btn btn-danger p-2 mx-3" onClick={toggleModal}>
          Delete Local Data
        </button>
      </nav>
      <div className="container-fluid custom-container">
        <div className="d-flex justify-content-center">
          <div className="row h-100 w-75">
            <div className="col-lg-3 mb-3 h-100">
              <div className="card h-100 overflow-auto">
                <div className="card-header">
                  <h5>Terminology</h5>
                </div>
                <div className="card-body d-flex justify-content-center align-content-center">
                  <div className="flex-grow-1 d-flex justify-content-center align-content-center">
                    <GoogleSheetReader
                      data={googleSheetData}
                      onFetchData={handleGoogleSheetData}
                      onOntologyTermClick={handleOntologyTermClick}
                      showList={showList}
                      onClose={handleSheetCloseClick}
                    />
                  </div>
                </div>
              </div>
            </div>

            <div className="col-lg-6 mb-3 h-100">
              <div className="card h-100 overflow-auto">
                <div className="card-header">
                  <h5>Mappings</h5>
                </div>
                <div className="card-body">
                  {selectedOntologyTerm && (
                    <div>
                      <h1 className="text-primary pb-3">{selectedOntologyTerm && selectedOntologyTerm.variable}</h1>
                      <p><b>Ontology Class: </b> {selectedOntologyTerm && selectedOntologyTerm.ontologyClass}</p>
                      <p><b>Data Type: </b> {selectedOntologyTerm && selectedOntologyTerm.type}</p>
                      <p><b>Unit: </b> {selectedOntologyTerm && selectedOntologyTerm.unit} {selectedOntologyTerm && selectedOntologyTerm.unitClass && '(' + selectedOntologyTerm.unitClass + ')'}</p>
                    </div>
                  )}
                  {selectedOntologyTerm && localTerms && localTerms.length > 0 && (
                    <div className="form-group">
                      <label htmlFor="columnSelect">Select Mapping:</label>
                      <select
                        id="columnSelect"
                        className="form-control"
                        value={selectedMapping}
                        onChange={handleMappingChange}
                      >
                        <option value="">Not Present</option>
                        {localTerms.map((column, index) => (
                          <option key={index} value={column}>
                            {column}
                          </option>
                        ))}
                      </select>
                    </div>
                  )}
                  {selectedMapping && selectedOntologyTerm && selectedOntologyTerm.valueClass && selectedOntologyTerm.valueClass.length > 0 && (
                    <CategoricalValues
                      csvData={csvData}
                      selectedOntologyTerm={selectedOntologyTerm}
                      selectedMapping={selectedMapping}
                    />
                  )}
                  {selectedMapping && selectedOntologyTerm && (selectedOntologyTerm.type === "float" || selectedOntologyTerm.type === "integer") && (
                    <div className="mt-3">
                      {(() => {
                        const stats = getColumnStatistics(selectedMapping);
                        return (
                          <div className="list-container">
                            <ul className="list-group p-0">
                              <li className="list-group-item">
                                <b>Mean:</b> {stats.mean}
                              </li>
                              <li className="list-group-item">
                                <b>Standard Deviation:</b> {stats.std}
                              </li>
                              <li className="list-group-item">
                                <b>Count:</b> {stats.count}
                              </li>
                              <li className="list-group-item">
                                <b>Min:</b> {stats.min}
                              </li>
                              <li className="list-group-item">
                                <b>Max:</b> {stats.max}
                              </li>
                            </ul>
                          </div>
                        );
                      })()}
                    </div>
                  )}
                </div>
              </div>
            </div>

            <div className="col-lg-3 mb-3 h-100">
              <div className="card h-100 overflow-auto">
                <div className="card-header">
                  <h5>Local Data</h5>
                </div>
                <div className="card-body">
                  <div className="flex-grow-1 d-flex justify-content-center m-3">
                    <CsvUploader
                      onUpload={handleCsvUpload}
                    />
                  </div>
                  <div className="d-flex justify-content-center">
                    <button className="btn btn-primary d-flex align-content-center p-3 my-2" onClick={handleExportJsonLd}>
                      Export JSON-LD
                    </button>

                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
