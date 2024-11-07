import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { OntologyTerm } from '../models/ontology-term';
import JsonLdService from '../services/JsonLdService';
import { ValueMapping } from '../models/value-mapping';

const CategoricalValues = ({ csvData, selectedOntologyTerm, selectedMapping, refreshJsonLdObject }) => {
  const CATEGORICAL = "categorical";
  const BOOLEAN = "boolean";

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
    assignCategoricalValueMappings(selectedOntologyTerm)
  }, [selectedOntologyTerm, selectedMapping]);

  const assignCategoricalValueMappings = (ontologyTerm: OntologyTerm | null) => {
    if (!ontologyTerm) return;
    if (ontologyTerm.type !== CATEGORICAL && ontologyTerm.type !== BOOLEAN) return;
    if(!ontologyTerm.unitIdentifiers || ontologyTerm.unitIdentifiers.length < 2) return; // Categorical variables and booleans should have at least 2 possible values
    const selectedCategoricalValues = new Map<string, any>();
    JsonLdService.getMapping(ontologyTerm.classIdentifier).then((mapping) => {
      ontologyTerm.unitIdentifiers.forEach((unitIdentifier: string) => {
        const valueMappings = mapping?.target?.value_mapping?.filter((valueMapping: ValueMapping) => valueMapping.target.uri === unitIdentifier) || [];
        const sources = valueMappings.map((valueMapping: ValueMapping) => valueMapping.source).filter(Boolean);
        selectedCategoricalValues.set(unitIdentifier, sources.length ? sources : []);
      });
      setCategoricalValueMappings(new Map<string, any>(selectedCategoricalValues)); // Force re-render
    });
  }
  const handleCategoricalValueSelectionChange = (index: number, event: any) => {
    event.preventDefault();
    event.stopPropagation();
    if (!selectedOntologyTerm) return;
    const targetUri = selectedOntologyTerm.unitIdentifiers[index];
    if (!targetUri || !event?.target?.value) return;

    const value = event.target.value;
    const hasValue = categoricalValueMappings.get(targetUri)?.includes(value);

    const updateMappings = () => {
      assignCategoricalValueMappings(selectedOntologyTerm);
      refreshJsonLdObject();
    };

    if (value === "not-present" && !hasValue) {
      JsonLdService.removeAllCategoricalValueMappingsForTargetUri(selectedOntologyTerm.classIdentifier, targetUri)
        .then(() => JsonLdService.addCategoricalValueMapping(selectedOntologyTerm.classIdentifier, value, targetUri))
        .then(updateMappings);
    } else if (hasValue) {
      JsonLdService.removeCategoricalValueMapping(selectedOntologyTerm.classIdentifier, value, targetUri)
        .then(updateMappings);
    } else {
      JsonLdService.removeCategoricalValueMapping(selectedOntologyTerm.classIdentifier, "not-present", targetUri)
        .then(() => JsonLdService.addCategoricalValueMapping(selectedOntologyTerm.classIdentifier, value, targetUri))
        .then(updateMappings);
    }
  };

  return (
    <div className="mt-3">
      {selectedOntologyTerm.unitIdentifiers && selectedOntologyTerm.unitIdentifiers.length > 1 && (
        <div className="table-responsive">
          <table className="table table-bordered">
            <thead>
              <tr>
                <th>Possible Categorical Values</th>
                <th>Local Name</th>
              </tr>
            </thead>
            <tbody>
              {
                Array.from(categoricalValueMappings.entries()).map((valueMapping: any, index: any, array) => {
                  return (
                    <tr key={valueMapping[0]}>
                      <td>
                        {selectedOntologyTerm.unitNames.length > index && selectedOntologyTerm.unitNames[index] ?
                      selectedOntologyTerm.unitNames[index] + ` (${valueMapping[0]})` : valueMapping[0]}</td>
                      <td>
                        <select multiple defaultValue={[]} value={valueMapping[1]} className="form-select"
                          onMouseDown={(event) => handleCategoricalValueSelectionChange(index, event)}
                          onChange={(event) => handleCategoricalValueSelectionChange(index, event)}>
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
