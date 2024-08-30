import React, { useEffect, useState } from 'react';
import CsvUploader from './components/CsvUploader.tsx';
import GoogleSheetReader from './components/GoogleSheetReader.tsx';
import CategoricalValues from './components/CategoricalValues.tsx';
import { mean, std, min, max } from 'mathjs';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.scss';
import JsonLdService from './services/JsonLdService.js';
import { OntologyTerm } from './models/ontology-term.ts';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import JsonLdPreviewOffcanvas from './components/JsonLdPreviewOffcanvas.tsx';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faFloppyDisk, faTrashCan } from '@fortawesome/free-regular-svg-icons';
import { Typeahead } from 'react-bootstrap-typeahead';
import 'react-bootstrap-typeahead/css/Typeahead.css';
import options from './assets/uo-terms.json';
import 'react-bootstrap-typeahead/css/Typeahead.css';
import 'react-bootstrap-typeahead/css/Typeahead.bs5.css';
import { UnitOntologyTerm } from './models/unit-ontology-term.ts';
import DateFormatSelect from './components/DateFormatSelect.tsx';

function App() {
  const [googleSheetData, setGoogleSheetData] = useState<OntologyTerm[]>([]);
  const [localTerms, setLocalTerms] = useState<string[]>([]);
  const [selectedOntologyTerm, setSelectedOntologyTerm] = useState<OntologyTerm | null>(null);
  const [showList, setShowList] = useState(false);
  const [selectedMapping, setSelectedMapping] = useState('');
  const [csvData, setCsvData] = useState(new Map<string, any>());
  const [csvFileName, setCsvFileName] = useState('');
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [isPreviewOffcanvasOpen, setIsPreviewOffcanvasOpen] = useState(false);
  const [jsonLdObject, setJsonLdObject] = useState({});
  const [localUnit, setLocalUnit] = useState<UnitOntologyTerm | undefined>();
  const [dateTimeFormat, setDateTimeFormat] = useState<string | undefined>();
  const [checkMarks, setCheckMarks] = useState<Map<string, boolean>>(new Map<string, boolean>());

  let _typeahead: any;

  const NOT_PRESENT = 'not-present';
  const FLOAT = "float";
  const INTEGER = "integer";
  const DATE = "date";

  useEffect(() => {
    JsonLdService.initDB();
  }, []);

  useEffect(() => {
    if(!selectedOntologyTerm) return;
    if(!localUnit){
      JsonLdService.deleteLocalUnit(selectedOntologyTerm.ontologyClass).then((jsonLdObject) => {
        setJsonLdObject(jsonLdObject);
      });
      return;
    } 
    JsonLdService.addLocalUnit(selectedOntologyTerm.ontologyClass, localUnit.preferredLabel, localUnit.classId).then((jsonLdObject) => {
      setJsonLdObject(jsonLdObject);
    });
  }, [selectedOntologyTerm, localUnit]);

  useEffect(() => {
    if(!selectedOntologyTerm) return;
    if(!dateTimeFormat){
      JsonLdService.deleteDateTimeFormat(selectedOntologyTerm.ontologyClass).then((jsonLdObject) => {
        setJsonLdObject(jsonLdObject);
      });
      return;
    } 
    JsonLdService.addDateTimeFormat(selectedOntologyTerm.ontologyClass, dateTimeFormat).then((jsonLdObject) => {
      setJsonLdObject(jsonLdObject);
    });
  }, [selectedOntologyTerm, dateTimeFormat]);

  useEffect(() => {
    determineCheckMarks(jsonLdObject);
  }, [jsonLdObject]);

  const determineCheckMarks = async (jsonLdObject) => {
    const checkMarks: Map<string, boolean> = new Map<string, boolean>();
    for(let ontologyTerm of googleSheetData) {
      const isMappingComplete = await JsonLdService.isMappingComplete(ontologyTerm.ontologyClass, ontologyTerm.valueClass);
      checkMarks.set(ontologyTerm.ontologyClass, isMappingComplete);
    }
    setCheckMarks(checkMarks);
  }

  const handleGoogleSheetData = (data: any) => {
    setGoogleSheetData(data);
    setShowList(true);
    refreshJsonLdObject();
  };

  const handleOntologyTermClick = (ontologyTerm: OntologyTerm) => {
    setSelectedOntologyTerm(ontologyTerm);
    JsonLdService.getMapping(ontologyTerm.ontologyClass).then((mapping) => {
      if (!mapping || !mapping.source || !mapping.source.column) {
        setSelectedMapping('');
      } else {
        setSelectedMapping(mapping.source.column);
        if(mapping.source.unit){
          setLocalUnit(options.find((option) => mapping.source.unit.uri === option.classId));
        } else {
          setLocalUnit({
            classId: undefined,
            preferredLabel: undefined,
            synonyms: undefined,
            definitions: undefined,
            obsolete: undefined,
            cui: undefined,
            semanticTypes: undefined,
            parents: undefined,
            hasRelatedSynonym: undefined
          });
        }
        if(mapping.source.dateTimeFormat){
          setDateTimeFormat(mapping.source.dateTimeFormat);
        } else {
          setDateTimeFormat(undefined);
        }
      }
    });
  };

  const handleSheetCloseClick = () => {
    setShowList(false);
    setSelectedOntologyTerm(null);
  };

  const handleCsvDataChange = (csvName: string, data: Map<string, any>) => {
    setCsvFileName(csvName);
    setCsvData(data);
    setLocalTerms(Array.from(data.keys()));
  }

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
        }).then(() => {
          JsonLdService.getJsonLdObject().then((jsonLdObject) => {
            setJsonLdObject(jsonLdObject);
          });
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
        ).then(() => {
          JsonLdService.getJsonLdObject().then((jsonLdObject) => {
            setJsonLdObject(jsonLdObject);
          });
        });
      }
    });
  };

  const getColumnStatistics = (column) => {
    if(!csvData.get(column)) {
      return {
        mean: 0,
        std: 0,
        count: 0,
        min: 0,
        max: 0,
      };
    }
    const columnData = csvData.get(column).map((value: any) => parseFloat(value))
      .filter((value: any) => !isNaN(value));
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
    setIsDeleteModalOpen(false);
    await JsonLdService.deleteJsonLdObject();
    JsonLdService.getJsonLdObject().then((jsonLdObject) => {
      setJsonLdObject(jsonLdObject);
    });
    if (!selectedOntologyTerm) return;
    handleOntologyTermClick(selectedOntologyTerm);
  }

  const toggleDeleteModal = () => {
    setIsDeleteModalOpen(!isDeleteModalOpen);
  };

  const togglePreviewOffcanvas = () => {
    refreshJsonLdObject();
    setIsPreviewOffcanvasOpen(!isPreviewOffcanvasOpen);
  }

  const refreshJsonLdObject = () => {
    JsonLdService.getJsonLdObject().then((jsonLdObject) => {
      setJsonLdObject(jsonLdObject);
    });
  }

  const changeLocalUnit = (selected: UnitOntologyTerm[]) => {
    if(!selected || selected.length === 0){
      setLocalUnit(undefined);
    } else {
      setLocalUnit(selected[0]);
    }
  }

  const changeLocalDateTimeFormat = (selected: string) => {
    if(!selected || selected.length === 0){
      setDateTimeFormat(undefined);
    } else {
      setDateTimeFormat(selected);
    }
  }

  const defocusLocalUnit = () => {
    if(!localUnit){
      if(!_typeahead) return;
      _typeahead.clear()
      _typeahead.focus()
    }
  }

  return (
    <div>
      <Modal show={isDeleteModalOpen} onHide={toggleDeleteModal}>
        <Modal.Header closeButton>
          <Modal.Title>Warning</Modal.Title>
        </Modal.Header>
        <Modal.Body>All mapping data will be deleted. Are you sure?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={toggleDeleteModal}>Cancel</Button>
          <Button variant="danger" onClick={deleteJsonLd}>Yes</Button>
        </Modal.Footer>
      </Modal>
      <JsonLdPreviewOffcanvas isOpen={isPreviewOffcanvasOpen} onToggle={togglePreviewOffcanvas} jsonLdObject={jsonLdObject} />
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
                      checkMarks={checkMarks}
                      onClose={handleSheetCloseClick}
                    />
                  </div>
                </div>
              </div>
            </div>

            <div className="col-lg-6 mb-3 h-100">
              <div className="card h-100 overflow-auto">
                <div className="card-header d-flex justify-content-between">
                  <h5>Mappings</h5>
                  <div>
                    <button className="btn btn-danger p-2 mx-1" onClick={toggleDeleteModal}>
                      <FontAwesomeIcon icon={faTrashCan} />
                    </button>
                    <button className="btn btn-primary p-2 mx-1" onClick={togglePreviewOffcanvas}>
                      <FontAwesomeIcon icon={faEye} />
                    </button>
                    <button className="btn btn-primary p-2 mx-1" onClick={handleExportJsonLd}>
                      <FontAwesomeIcon icon={faFloppyDisk} />
                    </button>
                  </div>
                </div>
                <div className="card-body">
                  {selectedOntologyTerm && (
                    <div>
                      <h1 className="text-primary pb-3">{selectedOntologyTerm && selectedOntologyTerm.variable}</h1>
                      <p><b>Ontology Class: </b> {selectedOntologyTerm && selectedOntologyTerm.ontologyClass}</p>
                      <p><b>Data Type: </b> {selectedOntologyTerm && selectedOntologyTerm.type}</p>
                      {/* <p><b>Unit: </b> {selectedOntologyTerm && options.find((option) => selectedOntologyTerm.unitClass === option.)?.preferredLabel} {selectedOntologyTerm && selectedOntologyTerm.unitClass && '(' + selectedOntologyTerm.unitClass + ')'}</p> */}
                    </div>
                  )}
                  {csvData && csvData.size > 0 && selectedOntologyTerm && localTerms && localTerms.length > 0 && (
                    <div className="form-group m-2">
                      <label htmlFor="columnSelect">Select Mapping:</label>
                      <select
                        id="columnSelect"
                        className="form-control"
                        value={selectedMapping}
                        onChange={handleMappingChange}
                      >
                        <option value="" disabled> Provide the Corresponding Local Value </option>
                        <option value="not-present">Not Present</option>
                        {localTerms.map((column, index) => (
                          <option key={index} value={column}>
                            {column}
                          </option>
                        ))}
                      </select>
                    </div>
                  )}
                  {csvData && csvData.size > 0 && selectedMapping && selectedOntologyTerm && selectedOntologyTerm.valueClass && selectedOntologyTerm.valueClass.length > 0 && (
                    <CategoricalValues
                      csvData={csvData}
                      selectedOntologyTerm={selectedOntologyTerm}
                      selectedMapping={selectedMapping}
                      refreshJsonLdObject={refreshJsonLdObject}
                    />
                  )}

                  {csvData && csvData.size > 0 && selectedMapping && selectedMapping !== NOT_PRESENT && selectedOntologyTerm && selectedOntologyTerm.type === DATE && (
                    <div className="form-group m-2">
                      <label htmlFor="local-unit-select">Select Local Date/Time Format Used:</label>
                      <DateFormatSelect selectedFormat={dateTimeFormat} onSelectChange={changeLocalDateTimeFormat}></DateFormatSelect>
                    </div>
                  )}

                  {csvData && csvData.size > 0 && selectedMapping && selectedMapping !== NOT_PRESENT && selectedOntologyTerm && (selectedOntologyTerm.type === FLOAT || selectedOntologyTerm.type === INTEGER) && (
                    <div className="form-group m-2">
                        <label htmlFor="local-unit-select">Select Local Unit Used:</label>
                        <Typeahead
                        id="local-unit-select"
                        ref={(ref) => _typeahead = ref}
                        labelKey="preferredLabel"
                        //@ts-ignore Unsure how to properly use typing here without casting
                        onChange={changeLocalUnit}
                        onBlur={defocusLocalUnit}
                        options={options}
                        placeholder="Select a local unit..."
                        //@ts-ignore Unsure how to properly use typing here without casting
                        selected={localUnit?.preferredLabel ? [localUnit] : []}
                      />
                    </div>
                  )}

                  {csvData && csvData.size > 0 && selectedMapping && selectedOntologyTerm && (selectedOntologyTerm.type === FLOAT || selectedOntologyTerm.type === INTEGER) && (
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

                  {(!csvData || csvData.size === 0) && (
                    <div className="my-5 text-center d-flex justify-content-center align-items-center">
                      <h3 className=" my-5 text-primary text-muted">Please Add Local Data</h3>
                    </div>
                  )}

                 {(csvData && csvData.size > 0 && !showList) && (
                    <div className="my-5 text-center d-flex justify-content-center align-items-center">
                      <h3 className=" my-5 text-primary text-muted">Please provide a Google Sheet with Terminology Data</h3>
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
                      onDataChange={handleCsvDataChange}
                    />
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
