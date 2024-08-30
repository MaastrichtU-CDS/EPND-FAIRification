import React, { useState } from 'react';
import axios from 'axios';
import Papa from 'papaparse';
import 'bootstrap/dist/css/bootstrap.min.css';
import { OntologyTerm } from '../models/ontology-term';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircleCheck, faCircleXmark } from '@fortawesome/free-regular-svg-icons';

export interface SheetReaderProps {
  data: OntologyTerm[];
  onFetchData: (data: any) => void;
  onOntologyTermClick: (term: OntologyTerm) => void;
  showList: boolean;
  checkMarks: Map<string, boolean>;
  onClose: () => void;
}

const GoogleSheetReader = ({ data, onFetchData, onOntologyTermClick, showList, checkMarks, onClose }: SheetReaderProps) => {
  const [sheetLink, setSheetLink] = useState('');
  const [loading, setLoading] = useState(false);
  const [unableToFetch, setUnableToFetch] = useState(false);

  const handleInputChange = (event) => {
    setSheetLink(event.target.value);
  };

  const fetchData = async (event) => {
    event.preventDefault();
    setLoading(true);
    setUnableToFetch(false);
    const sheetIdMatch = sheetLink.match(/\/spreadsheets\/d\/(.*?)\//);
    let gidMatch = sheetLink.match(/gid=(\d+)/);
    if(!gidMatch || gidMatch.length === 0) {
      gidMatch = ['0','0'];
    }
    if (sheetIdMatch && sheetIdMatch[1]) {
      const csvExportUrl = `https://docs.google.com/spreadsheets/d/${sheetIdMatch[1]}/export?gid=${gidMatch[1]}&format=csv`;
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
        setUnableToFetch(true);
      }
    } else {
      setLoading(false);
      setUnableToFetch(true);
    }
  };

  const isChecked = (termName:string): boolean | undefined => {
    return checkMarks.get(termName);
  }

  return (
    <div className="container d-flex h-100 w-100 align-items-center justify-content-center flex-column">
      {showList && !loading && !unableToFetch && (
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
      {showList && !loading && !unableToFetch && (
        <div className="h-100 w-100 p-3">
          <div className="list-container">
            <ul className="list-group">
              {data.map((item, index) => (
                <li
                  key={index}
                  className="list-group-item d-flex justify-content-between align-items-center"
                  style={{ cursor: 'pointer' }}
                  onClick={() => onOntologyTermClick(item)}
                >
                  <div>{item.variable}</div>
                  {checkMarks && checkMarks.size > 0 && isChecked(item.ontologyClass) && (
                    <div className='text-success'><FontAwesomeIcon icon={faCircleCheck} /></div>
                  )}
                  {checkMarks && checkMarks.size > 0 && !isChecked(item.ontologyClass) && (
                    <div className='text-danger'><FontAwesomeIcon icon={faCircleXmark} /></div>
                  )}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
      {unableToFetch && (
        <div className="alert alert-danger m-3" role="alert">
          Unable to fetch data from the provided Google Sheet. Please check the link and try again.
        </div>
      )}
    </div>
  );
};

export default GoogleSheetReader;