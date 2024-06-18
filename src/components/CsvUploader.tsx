import React, { useState, useRef } from 'react';
import Papa from 'papaparse';
import 'bootstrap/dist/css/bootstrap.min.css';
import './CsvUploader.css';

const CsvUploader = ({ onUpload }) => {
  const [data, setData] = useState([]);
  const [csvName, setCsvName] = useState('');
  const fileInputRef = useRef(null);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    parseCsv(file);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    parseCsv(file);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const parseCsv = (file) => {
    if (file) {
      Papa.parse(file, {
        header: true,
        complete: (result) => {
          setCsvName(file.name);
          setData(result.data);
          const columns = Object.keys(result.data[0]);
          onUpload(columns, result.data, file.name);
        },
      });
    }
  };

  const handleUploadAreaClick = () => {
    fileInputRef.current.click();
  };

  const onClose = () => {
    setData([]);
    setCsvName('');
    onUpload([], [], '');
  };

  return (
    <div className="container h-50">
      {!data.length ? (
        <div
          className="upload-area"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onClick={handleUploadAreaClick}
        >
          <p>Click or Drag and Drop a CSV here to update local data</p>
          <input
            type="file"
            accept=".csv"
            onChange={handleFileUpload}
            ref={fileInputRef}
            className="form-control-file"
            style={{ display: 'none' }}
          />
        </div>
      ) : (
        <div>
          <div className="w-100 d-flex justify-content-end">
            <button className="btn btn-close m-2" onClick={onClose}></button>
          </div>
          <p className="text-center text-primary fw-bold">{csvName}</p>
        </div>
      )}
    </div>
  );
};

export default CsvUploader;