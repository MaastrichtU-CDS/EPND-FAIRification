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
  const [sheetId, setSheetId] = useState('');
  const [spreadSheetId, setSpreadSheetId] = useState('');
  const [loading, setLoading] = useState(false);
  const [unableToFetch, setUnableToFetch] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const sheetInputChange = (event) => {
    setSheetId(event.target.value);
  }

  const spreadSheetInputChange = (event) => {
    setSpreadSheetId(event.target.value);
  }

  const fetchData = async (event) => {
    event.preventDefault();
    setLoading(true);
    setUnableToFetch(false);
    setErrorMessage('');

    const csvExportUrl = `https://docs.google.com/spreadsheets/d/${spreadSheetId}/export?gid=${sheetId}&format=csv`;
    try {
      const response = await axios.get(csvExportUrl);
      Papa.parse(response.data, {
        header: true,
        complete: (result) => {
          const parsedData: OntologyTerm[] = result.data.map((row: any) => ({
            classIdentifier: row['class identifier'],
            name: row.name,
            description: row.description,
            type: row.type,
            unitIdentifiers: row['unit identifiers']? row['unit identifiers'].replace(/\s/g, "").split(',') : [],
            unitNames: row['unit names']?.split(',').map(item => item.trim()) || []
          }));
          const invalidTerms = parsedData.filter(term => 
            !term.classIdentifier || !term.type || !term.name
          );
          if (invalidTerms.length > 0) {
            throw new Error('Some terms in the sheet have missing or empty fields for class identifier or type. Please make sure all terms have values for these fields.');
          }
          onFetchData(parsedData);
          setLoading(false);
        }
      });
    } catch (error) {
      console.error('Error fetching and parsing Google Sheet:', error);
      setLoading(false);
      setUnableToFetch(true);
      setErrorMessage(error.message);
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
              <input placeholder="Google Spreadsheet Id" type="text" className="form-control my-2" id="spreadSheetId" value={spreadSheetId} onChange={spreadSheetInputChange} />
              <input placeholder="Sheet Id" type="text" className="form-control my-2" id="sheetId" value={sheetId} onChange={sheetInputChange} />
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
                  <div>{item.name}</div>
                  {checkMarks && checkMarks.size > 0 && isChecked(item.classIdentifier) && (
                    <div className='text-success'><FontAwesomeIcon icon={faCircleCheck} /></div>
                  )}
                  {checkMarks && checkMarks.size > 0 && !isChecked(item.classIdentifier) && (
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
          Unable to fetch data from the provided Google Sheet: {errorMessage}
        </div>
      )}
    </div>
  );
};

export default GoogleSheetReader;