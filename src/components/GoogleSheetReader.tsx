import React, { useState } from 'react';
import axios from 'axios';
import Papa from 'papaparse';
import 'bootstrap/dist/css/bootstrap.min.css';
import { OntologyTerm } from '../models/ontology-term';

const GoogleSheetReader = ({ data, onFetchData, onOntologyTermClick, showList, onClose }) => {
  const [sheetLink, setSheetLink] = useState('');
  const [loading, setLoading] = useState(false);

  const handleInputChange = (event) => {
    setSheetLink(event.target.value);
  };

  const fetchData = async (event) => {
    event.preventDefault();
    setLoading(true);
    const sheetIdMatch = sheetLink.match(/\/spreadsheets\/d\/(.*?)\//);
    if (sheetIdMatch && sheetIdMatch[1]) {
      const csvExportUrl = `https://docs.google.com/spreadsheets/d/${sheetIdMatch[1]}/export?gid=0&format=csv`;

      try {
        const response = await axios.get(csvExportUrl);
        Papa.parse(response.data, {
          header: true,
          complete: (result) => {
            const parsedData: OntologyTerm = result.data.map(row => ({
              variable: row.Variables,
              ontologyClass: row.OntologyClass,
              unit: row.Unit,
              type: row.type,
              unitClass: row.unitClass,
              valueClass: row.ValueClass ? row.ValueClass.replace(/\s/g, "").split(',') : []
            }));
            onFetchData(parsedData);
            setLoading(false);
          }
        });
      } catch (error) {
        console.error('Error fetching and parsing Google Sheet:', error);
        setLoading(false);
      }
    }
  };

  return (
    <div className="container d-flex h-100 w-100 align-items-center justify-content-center flex-column">
      {showList && !loading && (
        <div className="w-100 d-flex justify-content-end">
          <button className="btn btn-close m-2" onClick={onClose}></button>
        </div>
      )}
      {!showList && !loading && (
        <form className="d-flex align-items-center" onSubmit={fetchData}>
          <div className="d-flex flex-column align-content-center">
            <div className="mb-3">
              <input placeholder="Google Sheet Link" type="text" className="form-control" id="sheetLink" value={sheetLink} onChange={handleInputChange} />
            </div>
            <button type="submit" className="btn btn-primary">Get Terminology</button>
          </div>
        </form>
      )}
      {loading && <div className="spinner-border text-primary" role="status">
        <span className="sr-only"></span>
      </div>}
      {showList && !loading && (
        <div className="h-100">
          <div className="list-container">
            <ul className="list-group">
              {data.map((item, index) => (
                <li
                  key={index}
                  className="list-group-item"
                  style={{ cursor: 'pointer' }}
                  onClick={() => onOntologyTermClick(item)}
                >
                  {item.variable}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default GoogleSheetReader;