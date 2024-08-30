import React, { useState, useRef, useEffect } from 'react';
import Papa from 'papaparse';
import 'bootstrap/dist/css/bootstrap.min.css';
import './CsvUploader.css';

const CsvUploader = ({ onDataChange }) => {
  const [csvData, setCsvData] = useState(new Map<string, any>());
  const [formOrder, setFormOrder] = useState<string[]>([]);
  const [displayColumnForm, setDisplayColumnForm] = useState(false);
  const [csvName, setCsvName] = useState('');
  const fileInputRef = useRef(null);

  useEffect(() => {
    onDataChange(csvName, csvData);
  }, [csvName, csvData]);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    setDisplayColumnForm(true);
    parseCsv(file);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    setDisplayColumnForm(true);
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
          const columns: any = Object.keys(result.data[0]);
          determineAndSetData(columns, result.data);
          const newFormOrder: string[] = [];
          Array.from(csvData.entries()).forEach((value, key) => {
            newFormOrder.push(value[0]);
          });
          setFormOrder(newFormOrder);
        },
      });
    }
  };

  const determineAndSetData = (columns: any, data: any) => {
    if (!columns || columns.length === 0 || !data || data.length === 0) {
      setCsvData(new Map<string, any>());
      return;
    }
    for (let column of columns) {
      const columnData = data
        .map((row) => row[column])
        .filter((value) => value !== null && value !== undefined && value !== '');
      csvData.set(column, [...new Set<string>(columnData)]);
      setCsvData(new Map<string, any>(csvData));
    }
  };


  const handleUploadAreaClick = () => {
    fileInputRef.current.click();
  };

  const toggleDisplayColumnForm = () => {
    setDisplayColumnForm(!displayColumnForm);
  }

  const deleteLocalData = () => {
    setDisplayColumnForm(false);
    setCsvData(new Map<string, any>());
    setFormOrder([]);
    setCsvName('');
  };

  const addColumn = () => {
    let newColumnName = `column-1`;
    for (let i = 1; formOrder.includes(newColumnName); i++) {
      newColumnName = `column-${i + 1}`;
    }
    const newCsvData = new Map([[newColumnName, []]]);
    csvData.forEach((value, key) => {
      newCsvData.set(key, value);
    });
  
    setCsvData(newCsvData);
    setFormOrder([newColumnName, ...formOrder]);
  };

  const removeColumn = (index, event) => {
    const columnName = formOrder[index];
    const newCsvData = new Map(csvData);
    newCsvData.delete(columnName);
    formOrder.splice(index, 1);
    setFormOrder(formOrder);
    setCsvData(newCsvData);
  }

  const setColumnName = (index, event) => {
    const columnName = event.target.value;
    const oldColumnName = event.target.id;
    const newCsvData = new Map(csvData);
    const columnData = csvData.get(oldColumnName);
    newCsvData.set(columnName, columnData);
    newCsvData.delete(oldColumnName);
    formOrder[index] = columnName;
    setFormOrder(formOrder);
    setCsvData(newCsvData);
  };

  const setUniqueCategoricalValues = (index, event) => {
    const newCsvData = new Map(csvData);
    const columnName = event.target.id;
    const newValues = event.target.value.split(',');
    newCsvData.set(columnName, newValues);
    formOrder[index] = columnName;
    setFormOrder(formOrder);
    setCsvData(newCsvData);
  };

  return (
    <div className="container h-50">
      {!displayColumnForm ? (
        <div>
          <div
            className="upload-area"
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onClick={handleUploadAreaClick}
          >
            <p>Click or Drag and Drop a CSV here to extract local data <br /><b>(Data is not uploaded, see the FAQ for more information)</b></p>
            <input
              type="file"
              accept=".csv"
              onChange={handleFileUpload}
              ref={fileInputRef}
              className="form-control-file"
              style={{ display: 'none' }}
            />
          </div>
          <div className="d-flex justify-content-center">
            <button className="btn btn-primary p-2 m-3" onClick={toggleDisplayColumnForm}>
              Manually Input Local Data
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div className="w-100 d-flex justify-content-center">
            <button className="btn btn-danger m-2" onClick={deleteLocalData}>Remove Local Data</button>
          </div>
          <div className="w-100 d-flex justify-content-center">
            <button className='btn btn-primary' onClick={addColumn}>Add Column</button>
          </div>
          {
            formOrder.map((columnName, index) => {
              let columnData = csvData.get(columnName);
              return (
                <div className='card card-body my-2' key={`column-${index}`}>
                  <div className="w-100 d-flex justify-content-end">
                    <button className="btn btn-close m-2" onClick={(event) => removeColumn(index, event)}></button>
                  </div>
                  <div>
                    <label htmlFor={columnName} className="form-label"><b>Column Name</b></label>
                    <input
                      type="text"
                      className="form-control my-2"
                      id={columnName}
                      value={columnName}
                      onChange={(event) => setColumnName(index, event)}
                    />
                    <label htmlFor={columnName} className="form-label"><b>Possible Values</b></label>
                    <input
                      type="text"
                      className="form-control"
                      id={columnName}
                      value={columnData ? columnData.join(',') : ''}
                      onChange={(event) => setUniqueCategoricalValues(index, event)}
                    />
                  </div>
                </div>
              )
            }
            )}
        </div>
      )}
    </div>
  );
};

export default CsvUploader;