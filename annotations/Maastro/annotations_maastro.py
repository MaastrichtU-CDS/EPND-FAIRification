import requests

endpoint = "http://rdf-store:7200/repositories/hn_one/statements"

query1 = """
PREFIX db: <http://hn_one.local/rdf/ontology/>
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
    
     db:hn1_clinical_data_updated_july_2020.years rdf:type owl:Class.  
   
     db:hn1_clinical_data_updated_july_2020.years rdfs:label "Years".
    
     db:hn1_clinical_data_updated_july_2020.days rdf:type owl:Class.
    
     db:hn1_clinical_data_updated_july_2020.days rdfs:label "Days".
    
     db:hn1_clinical_data_updated_july_2020.Gray rdf:type owl:Class. 
  
     db:hn1_clinical_data_updated_july_2020.Gray rdfs:label "Gy".
   
     db:hn1_clinical_data_updated_july_2020.radiotherapyClass rdf:type owl:Class.
    
     db:hn1_clinical_data_updated_july_2020.radiotherapyClass dbo:table db:hn1_clinical_data_updated_july_2020.
    
     db:hn1_clinical_data_updated_july_2020.radiotherapyClass rdfs:label "Radiotherapy".
     
     db:hn1_clinical_data_updated_july_2020.neoplasmClass rdf:type owl:Class. 
     
     db:hn1_clinical_data_updated_july_2020.neoplasmClass dbo:table db:hn1_clinical_data_updated_july_2020.
    
     db:hn1_clinical_data_updated_july_2020.neoplasmClass rdfs:label "Neoplasm".
    
     ?tablerow dbo:has_column ?neoplasm, ?radiotherapy.
    
     ?neoplasm rdf:type db:hn1_clinical_data_updated_july_2020.neoplasmClass.
    
     ?radiotherapy rdf:type db:hn1_clinical_data_updated_july_2020.radiotherapyClass.
  
}
}

where 
{
    BIND(IRI(CONCAT(str(?tablerow), "/neoplasm")) as ?neoplasm).
    
    BIND(IRI(CONCAT(str(?tablerow), "/radiotherapy")) as ?radiotherapy).
    
    ?tablerow rdf:type db:hn1_clinical_data_updated_july_2020.
   
}
        """

query2 = """
PREFIX db: <http://hn_one.local/rdf/ontology/>
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
        
	 ?tablerow roo:P100061 ?patientID.   #has_identifier
        
     ?tablerow roo:P100018 ?gender.		 #has_biological_sex
        
     ?tablerow roo:hasage ?age. 

     ?age roo:P100027 db:hn1_clinical_data_updated_july_2020.years.	
        
     ?tablerow roo:P100022 ?hpv.		 #has_finding
        
     ?tablerow roo:P100214 ?asa.		 #has_measurement
        
     ?tablerow roo:haswhostatus ?whostatus.   #has_WHO_status
        
     ?tablerow roo:P100029 ?neoplasm.
   
     ?neoplasm roo:P100244 ?tstage. 	 #has_T_stage
        
     ?neoplasm roo:P100242 ?nstage. 	 #has_N_stage
      
     ?neoplasm roo:P100241 ?mstage. 	 #has_M_stage
            
     ?neoplasm roo:P100219 ?ajcc. 		 #has_AJCC_stage
        
     ?neoplasm roo:P100202 ?tumour.		 #tumourSite
        
     ?neoplasm roo:P10032 ?metastasis. 	 #has_metastasis
        
     ?neoplasm roo:P100022 ?eventrecurrence, ?eventrecurrencedays, ?localrecurrence, ?localrecurrencedays, ?regionalrecurrence, ?regionalrecurrencedays, ?metastasisdays.  #has_finding
        
     ?localrecurrencedays roo:P100027 db:hn1_clinical_data_updated_july_2020.days.
        
     ?regionalrecurrencedays roo:P100027 db:hn1_clinical_data_updated_july_2020.days.
        
     ?metastasisdays roo:P100027 db:hn1_clinical_data_updated_july_2020.days.
        
     ?tablerow roo:P100403 ?radiotherapy. #treated_by 
        
     ?radiotherapy roo:P100027 ?rttotaldays. #has_unit
        
     ?rttotaldays roo:P100027 db:hn1_clinical_data_updated_july_2020.days.
        
     ?radiotherapy roo:P100023 ?graytotaldose. #has_dose
        
     ?graytotaldose roo:P100027 db:hn1_clinical_data_updated_july_2020.Gray.
        
     ?radiotherapy roo:P100214 ?graydoseperfraction.   #has_dose_per_fraction
     
     ?graydoseperfraction roo:P100027 db:hn1_clinical_data_updated_july_2020.Gray.
    
     ?radiotherapy roo:P100224 ?rtfractions. #has_fraction_count
      
     ?tablerow roo:P100403 ?surgery.     #treated_by
     
     ?tablerow roo:P100254 ?survival.    #has_death_finding 
        
     ?tablerow roo:has ?overallsurvivaldays.
        
     ?overallsurvivaldays roo:P100027 db:hn1_clinical_data_updated_july_2020.days.
        
     ?tablerow roo:P100231 ?chemo.        #chemo_administered
      
        
     db:hn1_clinical_data_updated_july_2020 owl:equivalentClass ncit:C16960.
        
     db:hn1_clinical_data_updated_july_2020.id owl:equivalentClass ncit:C25364.
        
     db:hn1_clinical_data_updated_july_2020.biological_sex owl:equivalentClass ncit:C28421.
        
     db:hn1_clinical_data_updated_july_2020.age_at_diagnosis owl:equivalentClass roo:C100003.
    
     db:hn1_clinical_data_updated_july_2020.overall_hpv_p16_status owl:equivalentClass ncit:C14226.
        
     db:hn1_clinical_data_updated_july_2020.pretreat_hb_in_mmolperlitre owl:equivalentClass roo:asaScore.
        
     db:hn1_clinical_data_updated_july_2020.performance_status_ecog owl:equivalentClass ncit:C105721.
        
     db:hn1_clinical_data_updated_july_2020.clin_t owl:equivalentClass ncit:C48885.
     
     db:hn1_clinical_data_updated_july_2020.clin_n owl:equivalentClass ncit:C48884.

	 db:hn1_clinical_data_updated_july_2020.clin_m owl:equivalentClass ncit:C48883.
        
     db:hn1_clinical_data_updated_july_2020.ajcc_stage owl:equivalentClass ncit:C38027.
        
     db:hn1_clinical_data_updated_july_2020.cancer_surgery_performed owl:equivalentClass ncit:C17173.
      
     db:hn1_clinical_data_updated_july_2020.index_tumour_location owl:equivalentClass ncit:C3263.
    
     db:hn1_clinical_data_updated_july_2020.event_recurrence_metastatic_free_survival owl:equivalentClass roo:eventrecurrence.
    
     db:hn1_clinical_data_updated_july_2020.recurrence_metastatic_free_survival_in_days owl:equivalentClass roo:eventrecurrencedays.
                
     db:hn1_clinical_data_updated_july_2020.event_local_recurrence owl:equivalentClass roo:localrecurrence.

	 db:hn1_clinical_data_updated_july_2020.local_recurrence_in_days owl:equivalentClass roo:localrecurrencedays.

	 db:hn1_clinical_data_updated_july_2020.event_locoregional_recurrence owl:equivalentClass roo:regionalrecurrence.

	 db:hn1_clinical_data_updated_july_2020.locoregional_recurrence_in_days owl:equivalentClass roo:regionalrecurrencedays.
        
     db:hn1_clinical_data_updated_july_2020.event_distant_metastases owl:equivalentClass ncit:C19151.
               
     db:hn1_clinical_data_updated_july_2020.distant_metastases_in_days owl:equivalentClass roo:metastasisdays.
        
     db:hn1_clinical_data_updated_july_2020.event_overall_survival owl:equivalentClass ncit:C25717.

	 db:hn1_clinical_data_updated_july_2020.overall_survival_in_days owl:equivalentClass roo:overallsurvivaldays.
        
     db:hn1_clinical_data_updated_july_2020.chemotherapy_given owl:equivalentClass ncit:C15632.
    
     db:hn1_clinical_data_updated_july_2020.radiotherapy_total_treat_time owl:equivalentClass roo:rttotaldays.
    
     db:hn1_clinical_data_updated_july_2020.radiotherapy_refgydose_total_highriskgtv owl:equivalentClass roo:graytotaldose.
        
     db:hn1_clinical_data_updated_july_2020.radiotherapy_refgydose_perfraction_highriskgtv owl:equivalentClass roo:graydoseperfraction.
    
     db:hn1_clinical_data_updated_july_2020.radiotherapy_number_fractions_highriskgtv owl:equivalentClass roo:rttotalfraction.
   
     db:hn1_clinical_data_updated_july_2020.years owl:equivalentClass ncit:C29848.
      
     db:hn1_clinical_data_updated_july_2020.days owl:equivalentClass ncit:C25301. 
    
     db:hn1_clinical_data_updated_july_2020.Gray owl:equivalentClass ncit:C18063.
    
     db:hn1_clinical_data_updated_july_2020.neoplasmClass owl:equivalentClass ncit:C3262.
    
     db:hn1_clinical_data_updated_july_2020.radiotherapyClass owl:equivalentClass ncit:C15313.
    
     dbo:has_value owl:sameAs roo:P100042.    #has_value
    
     dbo:has_unit owl:sameAs roo:P100047.    #has_value
     
     dbo:cell_of rdf:type owl:ObjectProperty;
                 owl:inverseOf dbo:has_cell.
       
    } 
}
  

WHERE

{  
    ?tablerow rdf:type db:hn1_clinical_data_updated_july_2020.
    
	?tablerow dbo:has_column ?patientID, ?gender, ?age, ?tumour, ?whostatus, ?hpv, ?tstage, ?nstage, ?mstage, ?ajcc, ?asa, ?surgery, ?chemo, ?rttotaldays, ?graytotaldose, ?graydoseperfraction, ?survival, ?overallsurvivaldays, ?localrecurrence, ?localrecurrencedays, ?regionalrecurrence, ?regionalrecurrencedays, ?metastasis, ?metastasisdays, ?neoplasm, ?radiotherapy, ?rtfractions, ?eventrecurrence, ?eventrecurrencedays.
          
    ?neoplasm rdf:type db:hn1_clinical_data_updated_july_2020.neoplasmClass.
    
    ?radiotherapy rdf:type db:hn1_clinical_data_updated_july_2020.radiotherapyClass. 
    
    ?patientID rdf:type db:hn1_clinical_data_updated_july_2020.id. 
 
    ?gender rdf:type db:hn1_clinical_data_updated_july_2020.biological_sex.
    
    ?age rdf:type db:hn1_clinical_data_updated_july_2020.age_at_diagnosis.
    
    ?tumour rdf:type db:hn1_clinical_data_updated_july_2020.index_tumour_location.
    
    ?whostatus rdf:type db:hn1_clinical_data_updated_july_2020.performance_status_ecog.
    
    ?hpv rdf:type db:hn1_clinical_data_updated_july_2020.overall_hpv_p16_status.
    
    ?tstage rdf:type db:hn1_clinical_data_updated_july_2020.clin_t.
    
    ?nstage rdf:type db:hn1_clinical_data_updated_july_2020.clin_n.
    
    ?mstage rdf:type db:hn1_clinical_data_updated_july_2020.clin_m.
    
    ?ajcc rdf:type db:hn1_clinical_data_updated_july_2020.ajcc_stage.
    
    ?asa rdf:type db:hn1_clinical_data_updated_july_2020.pretreat_hb_in_mmolperlitre.
    
    ?surgery rdf:type db:hn1_clinical_data_updated_july_2020.cancer_surgery_performed.
    
    ?chemo rdf:type db:hn1_clinical_data_updated_july_2020.chemotherapy_given.
    
    ?rttotaldays rdf:type db:hn1_clinical_data_updated_july_2020.radiotherapy_total_treat_time.
        
    ?graytotaldose rdf:type db:hn1_clinical_data_updated_july_2020.radiotherapy_refgydose_total_highriskgtv.
        
    ?graydoseperfraction rdf:type db:hn1_clinical_data_updated_july_2020.radiotherapy_refgydose_perfraction_highriskgtv.
    
    ?rtfractions rdf:type db:hn1_clinical_data_updated_july_2020.radiotherapy_number_fractions_highriskgtv.
        
    ?survival rdf:type db:hn1_clinical_data_updated_july_2020.event_overall_survival.
        
    ?overallsurvivaldays rdf:type db:hn1_clinical_data_updated_july_2020.overall_survival_in_days.
    
    ?eventrecurrence rdf:type db:hn1_clinical_data_updated_july_2020.event_recurrence_metastatic_free_survival.
        
    ?eventrecurrencedays rdf:type db:hn1_clinical_data_updated_july_2020.recurrence_metastatic_free_survival_in_days.
        
    ?localrecurrence rdf:type db:hn1_clinical_data_updated_july_2020.event_local_recurrence.
        
    ?localrecurrencedays rdf:type db:hn1_clinical_data_updated_july_2020.local_recurrence_in_days.
    
    ?regionalrecurrence rdf:type db:hn1_clinical_data_updated_july_2020.event_locoregional_recurrence.
    
    ?regionalrecurrencedays rdf:type db:hn1_clinical_data_updated_july_2020.locoregional_recurrence_in_days.
        
    ?metastasis rdf:type db:hn1_clinical_data_updated_july_2020.event_distant_metastases.
        
    ?metastasisdays rdf:type db:hn1_clinical_data_updated_july_2020.distant_metastases_in_days.
 
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
addMapping("female", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16576",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")
addMapping("male", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C20197",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")

# survival
addMapping("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28554",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")
addMapping("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C37987",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")
# 0=alive
# 1=dead

# tumorlocation
addMapping("oropharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping("larynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12420",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("hypopharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12246", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("nasopharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12423", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Base of tongue", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Tonsil", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Soft palate", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Glossopharyngeal sulcus", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")

# WHOstatus
addMapping("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105722",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105721")
addMapping("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105723",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105721")

# hpv
addMapping("positive", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping("negative", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C131488",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")

# ajcc
addMapping("i", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("ii", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("iii", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("iva", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("ivb", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("ivc", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

# chemo
addMapping("concomitant", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
addMapping("none", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15313",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
# addMapping("chemo radiation", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
# addMapping("Concurrent chemoradiotherapy", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
# addMapping("Induction chemotherapy+Radiation alone", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
# addMapping("Induction chemotherapy + concurrent chemoradiotherapy", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
