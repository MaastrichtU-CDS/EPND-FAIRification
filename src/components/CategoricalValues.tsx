import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { OntologyTerm } from '../models/ontology-term';
import JsonLdService from '../services/JsonLdService';
import { ValueMapping } from '../models/value-mapping';
import config from '../config/global-config.json';

const CategoricalValues = ({ csvData, selectedOntologyTerm, selectedMapping, refreshJsonLdObject }) => {
  const [categoricalValueMappings, setCategoricalValueMappings] = useState<Map<string, any>>(new Map<string, any>());
  const [uniqueCategoricalValues, setUniqueCategoricalValues] = useState<string[]>([]);

  useEffect(() => {
    const determineAndSetUniqueCategoricalValues = (selectedOntologyTerm: any, column: string) => {
      if (!column || column === "" || !selectedOntologyTerm || !csvData || csvData.length === 0){
        setUniqueCategoricalValues([]);
        return;
      } 
      let columnData = csvData.get(column);
      if(!columnData){
        setUniqueCategoricalValues([]);
        return;
      }
      columnData = columnData
        .filter((value) => value !== null && value !== undefined && value !== '');
      setUniqueCategoricalValues([...new Set<string>(columnData)]);
    };
    determineAndSetUniqueCategoricalValues(selectedOntologyTerm, selectedMapping);
  }, [selectedMapping, selectedOntologyTerm, csvData]);
  
  useEffect(() => {
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

    const determineLabels = (categoricalValueMappings: Map<string, any>): Promise<any>[] => {
      const promises: Promise<any>[] = [];
      categoricalValueMappings.forEach((value: any, key: string) => {
        promises.push(fetchOntologyTermLabel(key).then(label => {
            return [label, categoricalValueMappings.get(key)];
        }));
      });
      return promises;
    }

    assignCategoricalValueMappings(selectedOntologyTerm)
  }, [selectedOntologyTerm]);

  const handleCategoricalValueSelectionChange = (index: number, event: any) => {
    if (!selectedOntologyTerm) return;
    const targetUri = selectedOntologyTerm.valueClass[index];
    if (!targetUri) return;
    if (!event || !event.target) return;
    let value = event.target.value;
    if (!value) value = "";

    JsonLdService.addCategoricalValueMapping(selectedOntologyTerm.ontologyClass, event.target.value, targetUri).then(() => {
      refreshJsonLdObject();
    });
    fetchOntologyTermLabel(targetUri).then(label => {
      categoricalValueMappings.set(label, value);
      setCategoricalValueMappings(new Map<string, any>(categoricalValueMappings)); // Force re-render
    })
  };


  const fetchOntologyTermLabel = async (ontologyId) => {
    const query = encodeURIComponent(ontologyId).toUpperCase();
    const url = `${config.OLS_API_URL}/ontologies/snomed/terms?obo_id=${query}`;
    try {
      const response = await fetch(url, {
        headers: {
          'Accept': 'application/json'
        },
      });

      const responseJson = await response.json();
      if(!responseJson || !responseJson._embedded || !responseJson._embedded.terms || responseJson._embedded.terms.length === 0) {
        return ontologyId;
      }
      return responseJson._embedded.terms[0].label + ` (${ontologyId})`;
    } catch (error) {
      return ontologyId;
    }
  }
  
  return (
    <div className="mt-3">
      {selectedOntologyTerm.valueClass && selectedOntologyTerm.valueClass.length > 0 && (
        <div className="table-responsive" style={{ maxHeight: '400px', overflowY: 'auto' }}>
          <table className="table table-bordered">
            <thead>
              <tr>
                <th>Possible Categorical Values</th>
                <th>Local Name</th>
              </tr>
            </thead>
            <tbody>
              {
                Array.from(categoricalValueMappings.entries()).map((value: any, index: any, array) => {
                  return (
                    <tr key={value[0]}>
                      <td>{value[0]}</td>
                      <td>
                        <select value={value[1] !== undefined ? value[1] : undefined} className="form-select"
                          defaultValue={'DEFAULT'} onChange={(event) => handleCategoricalValueSelectionChange(index, event)}>
                          <option value="DEFAULT" disabled> Provide the Corresponding Local Value </option>
                          <option value="not-present">Not Present</option>                        
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
