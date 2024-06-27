import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { OntologyTerm } from '../models/ontology-term';
import JsonLdService from '../services/JsonLdService';
import { ValueMapping } from '../models/value-mapping';

const CategoricalValues = ({ csvData, selectedOntologyTerm, selectedMapping }) => {
  const [categoricalValueMappings, setCategoricalValueMappings] = useState<Map<string, any>>(new Map<string, any>());
  const [uniqueCategoricalValues, setUniqueCategoricalValues] = useState<string[]>([]);

  useEffect(() => {
    determineAndSetUniqueCategoricalValues(selectedOntologyTerm, selectedMapping);
  }, [selectedMapping, selectedOntologyTerm]);
  
  useEffect(() => {
    assignCategoricalValueMappings(selectedOntologyTerm)
  }, [selectedOntologyTerm]);

  
  const determineAndSetUniqueCategoricalValues = (selectedOntologyTerm: any, column: string) => {
    if (!column || column == "" || !selectedOntologyTerm || !csvData || csvData.length == 0) setUniqueCategoricalValues([]);
    const columnData = csvData
      .map((row) => row[column])
      .filter((value) => value !== null && value !== undefined && value !== '');
    setUniqueCategoricalValues([...new Set<string>(columnData)]);
  };

  const assignCategoricalValueMappings = (ontologyTerm: OntologyTerm | null) => {
    if (!ontologyTerm) return;

    const selectedCategoricalValues = new Map<string, any>();
    JsonLdService.getMapping(ontologyTerm.ontologyClass).then((mapping) => {
      ontologyTerm.valueClass.forEach((value, index) => {
        if (mapping && mapping.source && mapping.target && mapping.target.value_mapping) {
          const selectedCategoricalMapping = mapping.target.value_mapping.find((value_mapping: ValueMapping) => value_mapping.target.uri === value);
          if (selectedCategoricalMapping && selectedCategoricalMapping.source) {
            selectedCategoricalValues.set(value, selectedCategoricalMapping.source);
          } else {
            selectedCategoricalValues.set(value, null);
          }
        } else {
          selectedCategoricalValues.set(value, null);
        }
      });
      const promises = determineLabels(selectedCategoricalValues);
      Promise.all(promises).then((results:any) => {
        setCategoricalValueMappings(new Map<string, any>(results));
      });
    });
  }

  const handleCategoricalValueSelectionChange = (index: number, event: any) => {
    if (!selectedOntologyTerm) return;
    const targetUri = selectedOntologyTerm.valueClass[index];
    if (!targetUri) return;
    if (!event || !event.target) return;
    let value = event.target.value;
    if (!value) value = "";

    JsonLdService.addCategoricalValueMapping(selectedOntologyTerm.ontologyClass, event.target.value, targetUri).then(() => {
    });
    fetchOntologyTermLabel(targetUri).then(label => {
      categoricalValueMappings.set(label, value);
      setCategoricalValueMappings(new Map<string, any>(categoricalValueMappings)); // Force re-render
    })
  };


  const fetchOntologyTermLabel = async (ontologyId) => {
    const baseUrl = 'https://www.ebi.ac.uk/ols4/api';
    const query = encodeURIComponent(ontologyId).toUpperCase();
    const url = `${baseUrl}/ontologies/snomed/terms?obo_id=${query}`;
    try {
      const response = await fetch(url, {
        headers: {
          'Accept': 'application/json'
        },
      });

      const responseJson = await response.json();
      if(!responseJson || !responseJson._embedded || !responseJson._embedded.terms || responseJson._embedded.terms.length == 0) {
        return ontologyId;
      }
      return responseJson._embedded.terms[0].label + ` (${ontologyId})`;
    } catch (error) {
      return ontologyId;
    }
  }
  
  const determineLabels = (categoricalValueMappings: Map<string, any>): Promise<any>[] => {
    const promises: Promise<any>[] = [];
    categoricalValueMappings.forEach((value: any, key: string) => {
      promises.push(fetchOntologyTermLabel(key).then(label => {
          return [label, categoricalValueMappings.get(key)];
      }));
    });
    return promises;
  }

  return (
    <div className="mt-3">
      {selectedOntologyTerm.valueClass && selectedOntologyTerm.valueClass.length > 0 && (
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
                        <select value={value[1] ? value[1] : ""} className="form-select" onChange={(event) => handleCategoricalValueSelectionChange(index, event)}>
                          <option value="">Not Present</option>
                          {uniqueCategoricalValues.map((term : string, idx: number) => (
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
