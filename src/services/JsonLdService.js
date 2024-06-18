import { openDB } from 'idb';

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
    
    const existingCategoricalValueIndex = jsonLdObject.mappings[existingMappingIndex].target.value_mapping.findIndex(v => v.source === source);
    if (existingCategoricalValueIndex !== -1) {
      jsonLdObject.mappings[existingMappingIndex].target.value_mapping[existingCategoricalValueIndex] = { source, target };
    } else {
      jsonLdObject.mappings[existingMappingIndex].target.value_mapping.push({ source, target });
    }
    
    await this.saveJsonLdObject(jsonLdObject);
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
  }

  async addDatasource(database) {
    const jsonLdObject = await this.getJsonLdObject();
    const existingDatabase = jsonLdObject.databases.find(db => db.name === database.name);
    if (!existingDatabase) {
      jsonLdObject.databases.push(database);
      await this.saveJsonLdObject(jsonLdObject);
    }
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

export default new JsonLdService();
