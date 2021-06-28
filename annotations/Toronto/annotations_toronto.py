import requests

endpoint = "http://rdf-store:7200/repositories/opc/statements"

query1 = """
PREFIX db: <http://opc.local/rdf/ontology/>
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
    
     db:clinical_data_list_opc_v3.years rdf:type owl:Class.  
   
     db:clinical_data_list_opc_v3.years rdfs:label "Years".
    
     db:clinical_data_list_opc_v3.days rdf:type owl:Class.
    
     db:clinical_data_list_opc_v3.days rdfs:label "Days".
    
     db:clinical_data_list_opc_v3.Gray rdf:type owl:Class. 
  
     db:clinical_data_list_opc_v3.Gray rdfs:label "Gy".
   
     db:clinical_data_list_opc_v3.radiotherapyClass rdf:type owl:Class.
    
     db:clinical_data_list_opc_v3.radiotherapyClass dbo:table db:clinical_data_list_opc_v3.
   
     db:clinical_data_list_opc_v3.radiotherapyClass rdfs:label "Radiotherapy".
     
     db:clinical_data_list_opc_v3.neoplasmClass rdf:type owl:Class. 
     
     db:clinical_data_list_opc_v3.neoplasmClass dbo:table db:clinical_data_list_opc_v3.

     db:clinical_data_list_opc_v3.neoplasmClass rdfs:label "Neoplasm".
    
     ?tablerowTor dbo:has_column ?neoplasmTor, ?radiotherapyTor.
     
     ?neoplasmTor rdf:type db:clinical_data_list_opc_v3.neoplasmClass.
    
     ?radiotherapyTor rdf:type db:clinical_data_list_opc_v3.radiotherapyClass.
        
    }
}

where 
{
    BIND(IRI(CONCAT(str(?tablerowTor), "/neoplasm")) as ?neoplasmTor).
    
    BIND(IRI(CONCAT(str(?tablerowTor), "/radiotherapy")) as ?radiotherapyTor).
    
    ?tablerowTor rdf:type db:clinical_data_list_opc_v3.
   
}
        """

query2 = """
PREFIX db: <http://opc.local/rdf/ontology/>
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
        
	 ?tablerowTor roo:P100061 ?patientIDTor.   #has_identifier
        
     ?tablerowTor roo:P100018 ?genderTor.		 #has_biological_sex
        
     ?tablerowTor roo:hasage ?ageTor.  
    
     ?ageTor roo:P100027 db:clinical_data_list_opc_v3.years.	
        
     ?tablerowTor roo:P100022 ?hpvTor.		 #has_finding
     
     ?tablerowTor roo:has_smoking_status ?smokingTor.
    
     ?tablerowTor roo:P100229 ?followupdays.
    
     ?followupdays roo:P100027 db:clinical_data_list_opc_v3.days.
 
     ?tablerowTor roo:haswhostatus ?whostatusTor.   #has_WHO_status
        
     ?tablerowTor roo:P100029 ?neoplasmTor.
   
     ?neoplasmTor roo:P100244 ?tstageTor. 	 #has_T_stage
        
     ?neoplasmTor roo:P100242 ?nstageTor. 	 #has_N_stage
      
     ?neoplasmTor roo:P100241 ?mstageTor. 	 #has_M_stage
        
     ?neoplasmTor roo:P100219 ?ajccTor.
           
     ?neoplasmTor roo:P100202 ?tumourTor.		 #tumourSite
    
     ?neoplasmTor roo:P10032 ?metastasisTor. 	 #has_metastasis
        
     ?neoplasmTor roo:P100022 ?localrecurrenceTor, ?localrecurrencedaysTor, ?regionalrecurrenceTor, ?regionalrecurrencedaysTor, ?metastasisdaysTor.  #has_finding
        
     ?localrecurrencedaysTor roo:P100027 db:clinical_data_list_opc_v3.days.
        
     ?regionalrecurrencedaysTor roo:P100027 db:clinical_data_list_opc_v3.days.
        
     ?metastasisdaysTor roo:P100027 db:clinical_data_list_opc_v3.days.
   
     ?tablerowTor roo:P100403 ?radiotherapyTor. #treated_by
        
     ?radiotherapyTor roo:P100027 ?rttotaldaysTor. 
        
     ?rttotaldaysTor roo:P100027 db:clinical_data_list_opc_v3.days.
        
     ?radiotherapyTor roo:P100023 ?graytotaldoseTor. #has_dose
     
     ?radiotherapyTor roo:P100224 ?rtfractionsTor. #has_fraction_count
        
     ?graytotaldoseTor roo:P100027 db:clinical_data_list_opc_v3.Gray.
  
     ?tablerowTor roo:P100231 ?chemoTor.        #chemo_administered
    
     ?tablerowTor roo:P100254 ?survivalTor.    #has_death_finding
      
        
     db:clinical_data_list_opc_v3 owl:equivalentClass ncit:C16960.
        
     db:clinical_data_list_opc_v3.trial_patientid owl:equivalentClass ncit:C25364.
        
     db:clinical_data_list_opc_v3.sex owl:equivalentClass ncit:C28421.
        
     db:clinical_data_list_opc_v3.age_at_diagnosis owl:equivalentClass roo:C100003.
    
     db:clinical_data_list_opc_v3.hpv_p16_status_ihc owl:equivalentClass ncit:C14226.
        
     db:clinical_data_list_opc_v3.ecog_performance_status_scale owl:equivalentClass ncit:C105721.
        
     db:clinical_data_list_opc_v3.t owl:equivalentClass ncit:C48885.
     
     db:clinical_data_list_opc_v3.n owl:equivalentClass ncit:C48884.

	 db:clinical_data_list_opc_v3.m owl:equivalentClass ncit:C48883.
        
     db:clinical_data_list_opc_v3.stage_ajcc_7th_edition owl:equivalentClass ncit:C38027.
     
     db:clinical_data_list_opc_v3.smoking_hx owl:equivalentClass ncit:C156825.
        
     db:clinical_data_list_opc_v3.ds_site owl:equivalentClass ncit:C3263.
   
     db:clinical_data_list_opc_v3.interval_from_the_date_of_diagnosis_to_the_date_of_last_fu_days owl:equivalentClass roo:followupdays.
        
     db:clinical_data_list_opc_v3.chemotherapy owl:equivalentClass ncit:C15632.
    
     db:clinical_data_list_opc_v3.time_interval_from_the_date_of_diagnosis_to_the_rt_end_date_day owl:equivalentClass roo:rttotaldays.
    
     db:clinical_data_list_opc_v3.dose_gy owl:equivalentClass roo:graytotaldose.
     
     db:clinical_data_list_opc_v3.number_of_fractions owl:equivalentClass roo:rttotalfraction.
 
     db:clinical_data_list_opc_v3.status owl:equivalentClass ncit:C25717.
    
     db:clinical_data_list_opc_v3.local_failure owl:equivalentClass roo:localrecurrence.
    
     db:clinical_data_list_opc_v3.from_the_date_of_diagnosis_to_the_date_of_local_failure_days owl:equivalentClass roo:localrecurrencedays.

	 db:clinical_data_list_opc_v3.regional_failure owl:equivalentClass roo:regionalrecurrence.

     db:clinical_data_list_opc_v3.from_the_date_of_diagnosis_to_the_date_of_regional_failure_days owl:equivalentClass roo:regionalrecurrencedays.
        
     db:clinical_data_list_opc_v3.distant_failure owl:equivalentClass ncit:C19151.
     
     db:clinical_data_list_opc_v3.from_the_date_of_diagnosis_to_the_date_of_distant_failure_days owl:equivalentClass roo:metastasisdays.
   
     db:clinical_data_list_opc_v3.years owl:equivalentClass ncit:C29848.
      
     db:clinical_data_list_opc_v3.days owl:equivalentClass ncit:C25301. 
    
     db:clinical_data_list_opc_v3.Gray owl:equivalentClass ncit:C18063.
    
     db:clinical_data_list_opc_v3.neoplasmClass owl:equivalentClass ncit:C3262.
    
     db:clinical_data_list_opc_v3.radiotherapyClass owl:equivalentClass ncit:C15313.
    
     dbo:has_value owl:sameAs roo:P100042.    #has_value
    
     dbo:has_unit owl:sameAs roo:P100047.    #has_value
     
     dbo:cell_of rdf:type owl:ObjectProperty;
                 owl:inverseOf dbo:has_cell.
       
    } 
}
  
WHERE

{  
    ?tablerowTor rdf:type db:clinical_data_list_opc_v3.
    
	?tablerowTor dbo:has_column ?patientIDTor, ?genderTor, ?ageTor, ?hpvTor, ?whostatusTor, ?smokingTor, ?tstageTor, ?nstageTor, ?mstageTor, ?tumourTor, ?rttotaldaysTor, ?graytotaldoseTor, ?rtfractionsTor, ?chemoTor, ?followupdays, ?neoplasmTor, ?radiotherapyTor, ?survivalTor, ?metastasisTor, ?localrecurrenceTor, ?localrecurrencedaysTor, ?regionalrecurrenceTor, ?regionalrecurrencedaysTor, ?metastasisdaysTor, ?ajccTor.
          
    ?neoplasmTor rdf:type db:clinical_data_list_opc_v3.neoplasmClass.
    
    ?radiotherapyTor rdf:type db:clinical_data_list_opc_v3.radiotherapyClass. 
    
    ?patientIDTor rdf:type db:clinical_data_list_opc_v3.trial_patientid. 
 
    ?genderTor rdf:type db:clinical_data_list_opc_v3.sex.
    
    ?ageTor rdf:type db:clinical_data_list_opc_v3.age_at_diagnosis.
    
    ?tumourTor rdf:type db:clinical_data_list_opc_v3.ds_site.
    
    ?whostatusTor rdf:type db:clinical_data_list_opc_v3.ecog_performance_status_scale.
    
    ?smokingTor rdf:type db:clinical_data_list_opc_v3.smoking_hx.
    
    ?hpvTor rdf:type db:clinical_data_list_opc_v3.hpv_p16_status_ihc.
    
    ?tstageTor rdf:type db:clinical_data_list_opc_v3.t.
    
    ?nstageTor rdf:type db:clinical_data_list_opc_v3.n.
    
    ?mstageTor rdf:type db:clinical_data_list_opc_v3.m.
    
    ?ajccTor rdf:type db:clinical_data_list_opc_v3.stage_ajcc_7th_edition.
    
    ?chemoTor rdf:type db:clinical_data_list_opc_v3.chemotherapy.
    
    ?rttotaldaysTor rdf:type db:clinical_data_list_opc_v3.time_interval_from_the_date_of_diagnosis_to_the_rt_end_date_day.
        
    ?graytotaldoseTor rdf:type db:clinical_data_list_opc_v3.dose_gy.
        
    ?rtfractionsTor rdf:type db:clinical_data_list_opc_v3.number_of_fractions.
        
    ?followupdays rdf:type db:clinical_data_list_opc_v3.interval_from_the_date_of_diagnosis_to_the_date_of_last_fu_days.
    
    ?survivalTor rdf:type db:clinical_data_list_opc_v3.status.
    
    ?localrecurrenceTor rdf:type db:clinical_data_list_opc_v3.local_failure.
        
    ?localrecurrencedaysTor rdf:type db:clinical_data_list_opc_v3.from_the_date_of_diagnosis_to_the_date_of_local_failure_days.
    
    ?regionalrecurrenceTor rdf:type db:clinical_data_list_opc_v3.regional_failure.
    
    ?regionalrecurrencedaysTor rdf:type db:clinical_data_list_opc_v3.from_the_date_of_diagnosis_to_the_date_of_regional_failure_days.
        
    ?metastasisTor rdf:type db:clinical_data_list_opc_v3.distant_failure.
        
    ?metastasisdaysTor rdf:type db:clinical_data_list_opc_v3.from_the_date_of_diagnosis_to_the_date_of_distant_failure_days.
   
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
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX db: <http://hn_one.local/rdf/ontology/>
            PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
            INSERT {
                GRAPH <http://annotation.local/> {
                    ?term rdf:type owl:Class ;
          			 owl:equivalentClass [ owl:intersectionOf 
                									( [ rdf:type owl:Restriction ;
                                                        owl:onProperty dbo:cell_of ;
                                                        owl:someValuesFrom ?superClass;
                                                      ]
                                                      [ rdf:type owl:Restriction ;
                                                        owl:onProperty dbo:has_value ;
                                                        owl:hasValue ?localValue;
                                                      ]
                                                    ) ;
                                 rdf:type owl:Class
                               ] ;
          			 rdfs:subClassOf ?superClass .
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
addMapping("T0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48719",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("T1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48720",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("T2", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48724",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("T3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48728",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("T4a", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("T4b", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")

# N stage
addMapping("N0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48705",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("N1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48706",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("N2a", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("N2b", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("N2c", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("N3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48714",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")

# M stage
addMapping("M0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48699",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48883")
addMapping("M1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48700",
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
addMapping("Oropharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Larynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12420", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Hypopharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12246", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Nasopharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12423", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Base of tongue", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Tonsil", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Soft palate", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Glossopharyngeal sulcus", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")

# WHOstatus
addMapping("ECOG 0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105722",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105721")
addMapping("ECOG 1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105723",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105721")

#hpv
addMapping("  positive", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping("Positive", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping("Positive -Strong", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping("Positive -focal", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping("Negative", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C131488", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping("  Negative", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C131488", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")


# ajcc
addMapping("I", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("II", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("III", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("IVA", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("IVB", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

# chemo
addMapping("Yes", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
addMapping("none", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15313",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
# addMapping("chemo radiation", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
# addMapping("Concurrent chemoradiotherapy", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
# addMapping("Induction chemotherapy+Radiation alone", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
# addMapping("Induction chemotherapy + concurrent chemoradiotherapy", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
