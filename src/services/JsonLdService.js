import { openDB } from 'idb';

var FLOAT = 'float';
var INTEGER = 'integer';

class JsonLdService {
  db;

  constructor() {
    this.initDB();
  }

  async initDB() {
    this.db = await openDB('jsonLdDB', 1, {
      upgrade(db) {
        if (!db.objectStoreNames.contains('jsonLdStore')) {
          const store = db.createObjectStore('jsonLdStore', { keyPath: 'id' });
          store.put({ id: 1, jsonLdObject: { "@context": {}, "databases": [], "mappings": [] } });
        }
      }
    });
  }

  async getJsonLdObject() {
    if(!this.db) return;
    return (await this.db.get('jsonLdStore', 1)).jsonLdObject;
  }

  async getMapping(mappingUri){
    const jsonLdObject = await this.getJsonLdObject();
    if(!jsonLdObject.mappings) return null;
    const mappingIndex = jsonLdObject.mappings.findIndex(mapping => mapping.target.uri === mappingUri);
    if(mappingIndex === -1) return null;
    return jsonLdObject.mappings[mappingIndex];
  }

  async saveJsonLdObject(jsonLdObject) {
    await this.db.put('jsonLdStore', { id: 1, jsonLdObject });
  }

  async deleteJsonLdObject() {
    await this.db.put('jsonLdStore', { id: 1, jsonLdObject: { "@context": {}, "databases": [], "mappings": [] } });
  }

  // MappingUri is the uri of the target ontology term the categorical value is being mapped for.
  async addCategoricalValueMapping(mappingUri, source, targetUri) {
    const target = { uri: targetUri };
    const jsonLdObject = await this.getJsonLdObject();
    const existingMappingIndex = jsonLdObject.mappings.findIndex(mapping => mapping.target.uri === mappingUri);
    
    if (existingMappingIndex === -1) {
      throw new Error('Target mapping not found');
    }
    
    if (!jsonLdObject.mappings[existingMappingIndex].target.value_mapping) {
      jsonLdObject.mappings[existingMappingIndex].target.value_mapping = [];
    }
    
    const existingCategoricalValueIndex = jsonLdObject.mappings[existingMappingIndex].target.value_mapping.findIndex(v => {
      return v.target.uri === target.uri});
    if (existingCategoricalValueIndex !== -1) {
      jsonLdObject.mappings[existingMappingIndex].target.value_mapping[existingCategoricalValueIndex] = { source, target };
    } else {
      jsonLdObject.mappings[existingMappingIndex].target.value_mapping.push({ source, target });
    }
    await this.saveJsonLdObject(jsonLdObject);
    return jsonLdObject;
  }

  async addLocalUnit(selectedOntologyTerm, localUnitName, localUnitUri){
    if (!localUnitName || !localUnitUri) return;
    const jsonLdObject = await this.getJsonLdObject();
    const existingMappingIndex = jsonLdObject.mappings.findIndex(mapping => mapping.target.uri === selectedOntologyTerm);
    if (existingMappingIndex === -1) return;

    jsonLdObject.mappings[existingMappingIndex].source.unit = { uri: localUnitUri, name: localUnitName };
    await this.saveJsonLdObject(jsonLdObject);
    return jsonLdObject;
  }

  async deleteLocalUnit(selectedOntologyTerm){
    const jsonLdObject = await this.getJsonLdObject();
    const existingMappingIndex = jsonLdObject.mappings.findIndex(mapping => mapping.target.uri === selectedOntologyTerm);
    if (existingMappingIndex === -1) return;

    delete jsonLdObject.mappings[existingMappingIndex].source.unit;
    await this.saveJsonLdObject(jsonLdObject);
    return jsonLdObject;
  }

  async addDateTimeFormat(selectedOntologyTerm, dateTimeFormat) {
    if (!dateTimeFormat) return;
    const jsonLdObject = await this.getJsonLdObject();
    const existingMappingIndex = jsonLdObject.mappings.findIndex(mapping => mapping.target.uri === selectedOntologyTerm);
    if (existingMappingIndex === -1) return;
  
    jsonLdObject.mappings[existingMappingIndex].source.dateTimeFormat = dateTimeFormat;
    await this.saveJsonLdObject(jsonLdObject);
    return jsonLdObject;
  }
  
  async deleteDateTimeFormat(selectedOntologyTerm) {
    const jsonLdObject = await this.getJsonLdObject();
    const existingMappingIndex = jsonLdObject.mappings.findIndex(mapping => mapping.target.uri === selectedOntologyTerm);
    if (existingMappingIndex === -1) return;
  
    delete jsonLdObject.mappings[existingMappingIndex].source.dateTimeFormat;
    await this.saveJsonLdObject(jsonLdObject);
    return jsonLdObject;
  }

  async addMapping(source, target) {
    const jsonLdObject = await this.getJsonLdObject();
    const existingMappingIndex = jsonLdObject.mappings.findIndex(mapping => mapping.target.uri === target.uri);
    if (existingMappingIndex !== -1) {
      jsonLdObject.mappings[existingMappingIndex] = { source, target };
    } else {
      jsonLdObject.mappings.push({ source, target });
    }

    await this.saveJsonLdObject(jsonLdObject);
    return jsonLdObject;
  }

  async deleteMapping(target) {
    const jsonLdObject = await this.getJsonLdObject();
    const mappingIndex = jsonLdObject.mappings.findIndex(mapping => mapping.target.uri === target.uri);
    if (mappingIndex !== -1) {
      jsonLdObject.mappings.splice(mappingIndex, 1);
      await this.saveJsonLdObject(jsonLdObject);
    }
  }

  async addDatasource(database) {
    const jsonLdObject = await this.getJsonLdObject();
    const existingDatabase = jsonLdObject.databases.find(db => db.name === database.name);
    if (!existingDatabase) {
      jsonLdObject.databases.push(database);
      await this.saveJsonLdObject(jsonLdObject);
    }
  }

  async isMappingComplete(targetUri, valueClasses){
    if(!targetUri) return false;
    const jsonLdObject = await this.getJsonLdObject();
    const existingMappingIndex = jsonLdObject.mappings.findIndex(mapping => mapping.target.uri === targetUri);
    if (existingMappingIndex === -1) return false;
    const target = jsonLdObject.mappings[existingMappingIndex].target
    const source = jsonLdObject.mappings[existingMappingIndex].source
    if (target.value_mapping) {
      let valueMapped = false;
      for(const valueClass of valueClasses){
        valueMapped = false;
        for (const valueMapping of target.value_mapping) {  
          if(valueClass === valueMapping.target.uri){
            valueMapped = true;
          }
        }
      }
      if (!valueMapped) return false;
    }
    if(target.type.toLowerCase() === FLOAT || target.type.toLowerCase() === INTEGER){
      if(!source || !source.unit){
        return false;
      }
    }
    return true;
  }

  // Csv structure in the JSON-LD object will be reconsidered in the future, now opting for a database object without a schema where all columns are of type string.
  async addCsvDatasource(name, columns) {
    const database = {
      name: name,
      tables: [
        {
          name: name,
          columns: columns.map(column => ({ name: column, type: 'string' })),
          primary_key: columns[0],
          foreign_keys: []
        }
      ]
    };
    await this.addDatasource(database);
  }
}

let jsonLdService = new JsonLdService();
export default jsonLdService;
