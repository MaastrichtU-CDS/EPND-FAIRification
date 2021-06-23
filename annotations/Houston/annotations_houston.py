import requests

endpoint = "http://rdf-store:7200/repositories/hnscc/statements"

query1 = """
PREFIX db: <http://hnscc.local/rdf/ontology/>
PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

INSERT   
    {
     GRAPH <http://annotation.local/>
    {    
     db:hnscc_clinical_data.years rdf:type owl:Class.  
   
     db:hnscc_clinical_data.years rdfs:label "Years".
    
     db:hnscc_clinical_data.days rdf:type owl:Class.
    
     db:hnscc_clinical_data.days rdfs:label "Days".
    
     db:hnscc_clinical_data.Gray rdf:type owl:Class. 
  
     db:hnscc_clinical_data.Gray rdfs:label "Gy".
   
     db:hnscc_clinical_data.radiotherapyClass rdf:type owl:Class.
    
     db:hnscc_clinical_data.radiotherapyClass dbo:table db:hnscc_clinical_data.
    
	 db:hnscc_clinical_data.radiotherapyClass rdfs:label "Radiotherapy".
     
     db:hnscc_clinical_data.neoplasmClass rdf:type owl:Class. 
     
     db:hnscc_clinical_data.neoplasmClass dbo:table db:hnscc_clinical_data.
        
     db:hnscc_clinical_data.neoplasmClass rdfs:label "Neoplasm".
    
     ?tablerowHous dbo:has_column ?neoplasmHous, ?radiotherapyHous.
     
     ?neoplasmHous rdf:type db:hnscc_clinical_data.neoplasmClass.
    
     ?radiotherapyHous rdf:type db:hnscc_clinical_data.radiotherapyClass.
        
    } 
}
where 
{
    BIND(IRI(CONCAT(str(?tablerowHous), "/neoplasm")) as ?neoplasmHous).
    
    BIND(IRI(CONCAT(str(?tablerowHous), "/radiotherapy")) as ?radiotherapyHous).
    
    ?tablerowHous rdf:type db:hnscc_clinical_data.
   
}
        """

query2 = """
PREFIX db: <http://hnscc.local/rdf/ontology/>
PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

INSERT 
{
     GRAPH <http://annotation.local/>
    {      
	 ?tablerowHous roo:P100061 ?patientIDHous.   #has_identifier
     
     ?tablerowHous roo:hasage ?ageHous.  
    
     ?ageHous roo:P100027 db:hnscc_clinical_data.years.	
 
     ?tablerowHous roo:P100018 ?genderHous.
    
     ?tablerowHous roo:P100022 ?hpvHous.
    
     ?tablerowHous roo:P100029 ?neoplasmHous.
     
     ?neoplasmHous roo:P100219 ?ajccHous.
    
     ?neoplasmHous roo:P100244 ?tstageHous. 	
        
     ?neoplasmHous roo:P100242 ?nstageHous. 
        
     ?neoplasmHous roo:P100202 ?tumourHous.
    
     ?neoplasmHous roo:P10032 ?metastasisHous. 	 
    
     ?neoplasmHous roo:P100022 ?localrecurrenceHous, ?localrecurrencedaysHous, ?regionalrecurrenceHous, ?regionalrecurrencedaysHous, ?metastasisdaysHous. 
        
     ?localrecurrencedaysHous roo:P100027 db:hnscc_clinical_data.days.
        
     ?regionalrecurrencedaysHous roo:P100027 db:hnscc_clinical_data.days.
        
     ?metastasisdaysHous roo:P100027 db:hnscc_clinical_data.days.
        
     ?tablerowHous roo:P100403 ?radiotherapyHous. 
        
     ?radiotherapyHous roo:P100027 ?rttotaldaysHous. 
        
     ?rttotaldaysHous roo:P100027 db:hnscc_clinical_data.days.
        
     ?radiotherapyHous roo:P100023 ?graytotaldoseHous.
        
     ?graytotaldoseHous roo:P100027 db:hnscc_clinical_data.Gray.
        
     ?radiotherapyHous roo:P100214 ?graydoseperfractionHous.
     
     ?graydoseperfractionHous roo:P100027 db:hnscc_clinical_data.Gray.
    
     ?radiotherapyHous roo:P100224 ?rtfractionsHous.
    
     ?tablerowHous roo:P100254 ?survivalHous.
        
     ?tablerowHous roo:has ?overallsurvivaldaysHous.
    
     ?tablerowHous roo:P100229 ?followupHous.
    
     ?followupHous roo:P100027 db:hnscc_clinical_data.days.
        
     ?tablerowHous roo:P100231 ?chemoHous.
       
    
     db:hnscc_clinical_data owl:equivalentClass ncit:C16960.
        
     db:hnscc_clinical_data.tcia_radiomics_id owl:equivalentClass ncit:C25364.
            
     db:hnscc_clinical_data.age_at_diag owl:equivalentClass roo:C100003.
    
     db:hnscc_clinical_data.gender owl:equivalentClass ncit:C28421.
    
     db:hnscc_clinical_data.hpv_status owl:equivalentClass ncit:C14226.
    
     db:hnscc_clinical_data.ajcc_stage_7th_edition owl:equivalentClass ncit:C38027.
    
     db:hnscc_clinical_data.cancer_subsite_of_origin owl:equivalentClass ncit:C3263.
    
     db:hnscc_clinical_data.t_category owl:equivalentClass ncit:C48885.
     
     db:hnscc_clinical_data.n_category owl:equivalentClass ncit:C48884.
    
     db:hnscc_clinical_data.radiation_treatment_duration owl:equivalentClass roo:rttotaldays.
    
     db:hnscc_clinical_data.total_prescribed_radiation_treatment_dose owl:equivalentClass roo:graytotaldose.
        
     db:hnscc_clinical_data.radiation_treatment_dose_per_fraction owl:equivalentClass roo:graydoseperfraction.
    
     db:hnscc_clinical_data.radiation_treatment_number_of_fractions owl:equivalentClass roo:rttotalfraction.
    
     db:hnscc_clinical_data.vital_status owl:equivalentClass ncit:C25717.

	 db:hnscc_clinical_data.overall_survival_duration owl:equivalentClass roo:overallsurvivaldays.
    
     db:hnscc_clinical_data.local_control owl:equivalentClass roo:localrecurrence.

	 db:hnscc_clinical_data.local_control_duration owl:equivalentClass roo:localrecurrencedays.

	 db:hnscc_clinical_data.regional_control owl:equivalentClass roo:regionalrecurrence.

	 db:hnscc_clinical_data.regional_control_duration owl:equivalentClass roo:regionalrecurrencedays.
        
     db:hnscc_clinical_data.freedom_from_distant_metastasis owl:equivalentClass ncit:C19151.
               
     db:hnscc_clinical_data.freedom_from_distant_metastasis_duration owl:equivalentClass roo:metastasisdays.
    
     db:hnscc_clinical_data.days_to_last_fu owl:equivalentClass roo:followupdays.
        
     db:hnscc_clinical_data.therapeutic_combination owl:equivalentClass ncit:C15632.
    
     db:hnscc_clinical_data.years owl:equivalentClass ncit:C29848.
      
     db:hnscc_clinical_data.days owl:equivalentClass ncit:C25301. 
    
     db:hnscc_clinical_data.Gray owl:equivalentClass ncit:C18063.
    
     db:hnscc_clinical_data.neoplasmClass owl:equivalentClass ncit:C3262.
    
     db:hnscc_clinical_data.radiotherapyClass owl:equivalentClass ncit:C15313.
    
     dbo:has_value owl:sameAs roo:P100042.    #has_value
    
     dbo:has_unit owl:sameAs roo:P100047.    #has_value
       
    } 
}
WHERE
{  
    ?tablerowHous rdf:type db:hnscc_clinical_data.
    
	?tablerowHous dbo:has_column ?patientIDHous, ?ageHous, ?genderHous, ?hpvHous, ?ajccHous, ?tumourHous, ?neoplasmHous, ?radiotherapyHous, ?tstageHous, ?nstageHous, ?rttotaldaysHous, ?graytotaldoseHous, ?graydoseperfractionHous, ?rtfractionsHous, ?survivalHous, ?overallsurvivaldaysHous, ?metastasisHous, ?localrecurrenceHous, ?localrecurrencedaysHous, ?regionalrecurrenceHous, ?regionalrecurrencedaysHous, ?metastasisdaysHous, ?followupHous, ?chemoHous.
    
    ?neoplasmHous rdf:type db:hnscc_clinical_data.neoplasmClass.
    
    ?radiotherapyHous rdf:type db:hnscc_clinical_data.radiotherapyClass. 
    
    ?patientIDHous rdf:type db:hnscc_clinical_data.tcia_radiomics_id. 
 
    ?ageHous rdf:type db:hnscc_clinical_data.age_at_diag.
    
    ?genderHous rdf:type db:hnscc_clinical_data.gender.
    
    ?hpvHous rdf:type db:hnscc_clinical_data.hpv_status.
    
    ?tumourHous rdf:type db:hnscc_clinical_data.cancer_subsite_of_origin.
    
    ?ajccHous rdf:type db:hnscc_clinical_data.ajcc_stage_7th_edition.
    
    ?tstageHous rdf:type db:hnscc_clinical_data.t_category.
        
    ?nstageHous rdf:type db:hnscc_clinical_data.n_category.
    
    ?rttotaldaysHous rdf:type db:hnscc_clinical_data.radiation_treatment_duration. 
    
    ?graytotaldoseHous rdf:type db:hnscc_clinical_data.total_prescribed_radiation_treatment_dose.
            
    ?graydoseperfractionHous rdf:type db:hnscc_clinical_data.radiation_treatment_dose_per_fraction.
    
    ?rtfractionsHous rdf:type db:hnscc_clinical_data.radiation_treatment_number_of_fractions.
    
    ?survivalHous rdf:type db:hnscc_clinical_data.vital_status.
        
    ?overallsurvivaldaysHous rdf:type db:hnscc_clinical_data.overall_survival_duration.
    
    ?metastasisHous rdf:type db:hnscc_clinical_data.freedom_from_distant_metastasis.
     
    ?localrecurrenceHous rdf:type db:hnscc_clinical_data.local_control.
            
    ?localrecurrencedaysHous rdf:type db:hnscc_clinical_data.local_control_duration.
    
    ?regionalrecurrenceHous rdf:type db:hnscc_clinical_data.regional_control.
    
    ?regionalrecurrencedaysHous rdf:type db:hnscc_clinical_data.regional_control_duration.
    
    ?metastasisdaysHous rdf:type db:hnscc_clinical_data.freedom_from_distant_metastasis_duration.
    
    ?followupHous rdf:type db:hnscc_clinical_data.days_to_last_fu.
    
    ?chemoHous rdf:type db:hnscc_clinical_data.therapeutic_combination. 
}
"""

def runQuery1(endpoint, query1):
    annotationResponse = requests.post(endpoint,
                                       data="update=" + query1,
                                       headers={
                                           "Content-Type": "application/x-www-form-urlencoded",
                                           # "Accept": "application/json"
                                       })
    output = annotationResponse.text
    print(output)

def runQuery2(endpoint, query2):
    annotationResponse = requests.post(endpoint,
                                       data="update=" + query2,
                                       headers={
                                           "Content-Type": "application/x-www-form-urlencoded",
                                           # "Accept": "application/json"
                                       })
    output = annotationResponse.text
    print(output)

runQuery1(endpoint, query1)
runQuery2(endpoint, query2)

def addMapping(localTerm, targetClass, superClass):
    query = """
     PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            INSERT {
                GRAPH <http://annotation.local/> {
                    ?term owl:equivalentClass [
                        rdf:type owl:Class;
                        owl:intersectionOf [
                            rdf:first ?superClass;
                            rdf:rest [
                                rdf:first [
                                    rdf:type owl:Class;
                                    owl:unionOf [
                                        rdf:first [
                                            rdf:type owl:Restriction;
                                            owl:hasValue ?localValue;
                                            owl:onProperty <http://um-cds/ontologies/databaseontology/has_value>;
                                        ];
                                        rdf:rest rdf:nil;
                                    ]
                                ];
                                rdf:rest rdf:nil;
                            ]
                        ]
                    ].
                }
            } WHERE { 
                BIND(<%s> AS ?term).
                BIND(<%s> AS ?superClass).
                BIND("%s"^^xsd:string AS ?localValue).

            }
            """ % (targetClass, superClass, localTerm)

    annotationResponse = requests.post(endpoint,
                                       data="update=" + query,
                                       headers={
                                           "Content-Type": "application/x-www-form-urlencoded"
                                       })
    print(annotationResponse.status_code)


# T stage
addMapping("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48719",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48720",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("2", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48724",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48728",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("4", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
# addMapping("T4b", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")


# N stage
addMapping("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48705",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48706",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("2", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
# addMapping("N2b", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
# addMapping("N2c", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48714",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")

# M stage
addMapping("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48699",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48883")
addMapping("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48700",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48883")

# gender
addMapping("Female", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16576",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")
addMapping("Male", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C20197",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")

# survival
addMapping("Dead", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28554",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")
addMapping("Alive", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C37987",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")
# 0=alive
# 1=dead

# tumorlocation
# addMapping("Oropharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Larynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12420", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Hypopharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12246", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Nasopharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12423", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping("Base of tongue", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping("Tonsil", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping("Soft palate", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping("Glossopharyngeal sulcus", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")

# WHOstatus
# addMapping("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105722", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105721")
# addMapping("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105723", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105721")

# hpv
addMapping("P", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping("N", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C131488",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")

# ajcc
addMapping("I", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("II", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("III", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("IV", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

# chemo
# addMapping("chemo radiation", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
addMapping("Radiation alone", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15313",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
# addMapping("chemo radiation", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
addMapping("Concurrent chemoradiotherapy", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
addMapping("Induction chemotherapy%2BRadiation alone", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
addMapping("Induction chemotherapy %2B concurrent chemoradiotherapy",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")