import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const CategoricalValues = ({ data, categoricalValueMappings, uniqueCategoricalValues, onSelectionChange }) => {
  
  const handleSelectChange = (index, event) => {
    onSelectionChange(index, event);
  };
  return (
    <div className="mt-3">
      {data.valueClass && data.valueClass.length > 0 && (
        <div className="table-responsive" style={{ maxHeight: '400px', overflowY: 'auto' }}>
          <table className="table table-bordered">
            <thead>
              <tr>
                <th>Possible Categorical Values</th>
                <th>Values Found in Data</th>
              </tr>
            </thead>
            <tbody>
              {
                Array.from(categoricalValueMappings.entries()).map((value: any, index: any, array) => {
                  return (
                    <tr key={value[0]}>
                      <td>{value[0]}</td>
                      <td>
                        <select value={value[1] ? value[1] : ""} className="form-select" onChange={(event) => handleSelectChange(index, event)}>
                          <option value="">Not Present</option>
                          {uniqueCategoricalValues.map((term : string, idx: string) => (
                            <option key={idx} value={term}>{term}</option>
                          ))}
                        </select>
                      </td>
                    </tr>
                  );
                })
              }
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default CategoricalValues;
