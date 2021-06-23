import requests

endpoint = "http://rdf-store:7200/repositories/head_neck/statements"

query1 = """
PREFIX db: <http://head_neck.local/rdf/ontology/>
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
    
     db:infoclinical_hn_version2_30may2018_concat.years rdf:type owl:Class.  
   
     db:infoclinical_hn_version2_30may2018_concat.years rdfs:label "Years".
    
     db:infoclinical_hn_version2_30may2018_concat.days rdf:type owl:Class.
    
     db:infoclinical_hn_version2_30may2018_concat.days rdfs:label "Days".
    
     db:infoclinical_hn_version2_30may2018_concat.Gray rdf:type owl:Class. 
  
     db:infoclinical_hn_version2_30may2018_concat.Gray rdfs:label "Gy".
   
     db:infoclinical_hn_version2_30may2018_concat.radiotherapyClass rdf:type owl:Class.
    
     db:infoclinical_hn_version2_30may2018_concat.radiotherapyClass dbo:table db:infoclinical_hn_version2_30may2018_concat.
    
     db:infoclinical_hn_version2_30may2018_concat.radiotherapyClass rdfs:label "Radiotherapy".
     
     db:infoclinical_hn_version2_30may2018_concat.neoplasmClass rdf:type owl:Class. 
     
     db:infoclinical_hn_version2_30may2018_concat.neoplasmClass dbo:table db:infoclinical_hn_version2_30may2018_concat.
     
     db:infoclinical_hn_version2_30may2018_concat.neoplasmClass rdfs:label "Neoplasm".
    
     ?tablerowMon dbo:has_column ?neoplasmMon, ?radiotherapyMon.
     
     ?neoplasmMon rdf:type db:infoclinical_hn_version2_30may2018_concat.neoplasmClass.
    
     ?radiotherapyMon rdf:type db:infoclinical_hn_version2_30may2018_concat.radiotherapyClass.
    } 
}

where 
{
    BIND(IRI(CONCAT(str(?tablerowMon), "/neoplasm")) as ?neoplasmMon).
    
    BIND(IRI(CONCAT(str(?tablerowMon), "/radiotherapy")) as ?radiotherapyMon).
    
    ?tablerowMon rdf:type db:infoclinical_hn_version2_30may2018_concat.
   
}
        """

query2 = """
PREFIX db: <http://head_neck.local/rdf/ontology/>
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
        
	 ?tablerowMon roo:P100061 ?patientIDMon.   #has_identifier
        
     ?tablerowMon roo:P100018 ?genderMon.		 #has_biological_sex
        
     ?tablerowMon roo:hasage ?ageMon. 
    
     ?ageMon roo:P100027 db:infoclinical_hn_version2_30may2018_concat.years.	
        
     ?tablerowMon roo:P100022 ?hpvMon.		 #has_finding
   
     ?tablerowMon roo:P100229 ?followupMon.
        
     ?tablerowMon roo:P100029 ?neoplasmMon.
   
     ?neoplasmMon roo:P100244 ?tstageMon. 	 #has_T_stage
        
     ?neoplasmMon roo:P100242 ?nstageMon. 	 #has_N_stage
      
     ?neoplasmMon roo:P100241 ?mstageMon. 	 #has_M_stage
        
     ?neoplasmMon roo:P100219 ?ajccMon.
    
     ?neoplasmMon roo:P100202 ?tumourMon.		 #tumourSite
        
     ?neoplasmMon roo:P10032 ?metastasisMon. 	 #has_metastasis
        
     ?neoplasmMon roo:P100022 ?regionalrecurrenceMon, ?regionalrecurrencedaysMon, ?metastasisdaysMon.  #has_finding
    
     ?regionalrecurrencedaysMon roo:P100027 db:infoclinical_hn_version2_30may2018_concat.days.
        
     ?metastasisdaysMon roo:P100027 db:infoclinical_hn_version2_30may2018_concat.days.
        
     ?tablerowMon roo:P100403 ?radiotherapyMon. #treated_by 
    
     ?tablerowMon roo:P100403 ?surgeryMon.     #treated_by
     
     ?tablerowMon roo:P100254 ?survivalMon.    #has_death_finding 
        
     ?tablerowMon roo:has ?overallsurvivaldaysMon.
        
     ?overallsurvivaldaysMon roo:P100027 db:infoclinical_hn_version2_30may2018_concat.days.
        
     ?tablerowMon roo:P100231 ?chemoMon. 
    
    
     db:infoclinical_hn_version2_30may2018_concat owl:equivalentClass ncit:C16960.
        
     db:infoclinical_hn_version2_30may2018_concat.patient owl:equivalentClass ncit:C25364.
        
     db:infoclinical_hn_version2_30may2018_concat.sex owl:equivalentClass ncit:C28421.
        
     db:infoclinical_hn_version2_30may2018_concat.age owl:equivalentClass roo:C100003.
    
     db:infoclinical_hn_version2_30may2018_concat.hpv_status owl:equivalentClass ncit:C14226.
    
     db:infoclinical_hn_version2_30may2018_concat.time_diagnosis_to_last_follow_up_days owl:equivalentClass roo:followupdays.
        
     db:infoclinical_hn_version2_30may2018_concat.t_stage owl:equivalentClass ncit:C48885.
     
     db:infoclinical_hn_version2_30may2018_concat.n_stage owl:equivalentClass ncit:C48884.

	 db:infoclinical_hn_version2_30may2018_concat.m_stage owl:equivalentClass ncit:C48883.
        
     db:infoclinical_hn_version2_30may2018_concat.tnm_group_stage owl:equivalentClass ncit:C38027.
    
     db:infoclinical_hn_version2_30may2018_concat.surgery owl:equivalentClass ncit:C17173.
      
     db:infoclinical_hn_version2_30may2018_concat.primary_site owl:equivalentClass ncit:C3263.
    
	 db:infoclinical_hn_version2_30may2018_concat.locoregional owl:equivalentClass roo:regionalrecurrence.

	 db:infoclinical_hn_version2_30may2018_concat.time_diagnosis_to_lr_days owl:equivalentClass roo:regionalrecurrencedays.
        
     db:infoclinical_hn_version2_30may2018_concat.distant owl:equivalentClass ncit:C19151.
               
     db:infoclinical_hn_version2_30may2018_concat.time_diagnosis_to_dm_days owl:equivalentClass roo:metastasisdays.
        
     db:infoclinical_hn_version2_30may2018_concat.death owl:equivalentClass ncit:C25717.

	 db:infoclinical_hn_version2_30may2018_concat.time_diagnosis_to_death_days owl:equivalentClass roo:overallsurvivaldays.
        
     db:infoclinical_hn_version2_30may2018_concat.therapy owl:equivalentClass ncit:C15632.

     db:infoclinical_hn_version2_30may2018_concat.years owl:equivalentClass ncit:C29848.
      
     db:infoclinical_hn_version2_30may2018_concat.days owl:equivalentClass ncit:C25301. 
    
     db:infoclinical_hn_version2_30may2018_concat.Gray owl:equivalentClass ncit:C18063.
    
     db:infoclinical_hn_version2_30may2018_concat.neoplasmClass owl:equivalentClass ncit:C3262.
    
     db:infoclinical_hn_version2_30may2018_concat.radiotherapyClass owl:equivalentClass ncit:C15313.
    
     dbo:has_value owl:sameAs roo:P100042.    #has_value
    
     dbo:has_unit owl:sameAs roo:P100047.    #has_value
       
    } 
}  

WHERE

{  
    ?tablerowMon rdf:type db:infoclinical_hn_version2_30may2018_concat.
    
	?tablerowMon dbo:has_column ?patientIDMon, ?genderMon, ?ageMon, ?tumourMon, ?hpvMon, ?tstageMon, ?nstageMon, ?mstageMon, ?surgeryMon, ?survivalMon, ?overallsurvivaldaysMon, ?regionalrecurrenceMon, ?regionalrecurrencedaysMon, ?metastasisMon, ?metastasisdaysMon, ?followupMon, ?neoplasmMon, ?radiotherapyMon, ?ajccMon, ?chemoMon.
          
    ?neoplasmMon rdf:type db:infoclinical_hn_version2_30may2018_concat.neoplasmClass.
    
    ?radiotherapyMon rdf:type db:infoclinical_hn_version2_30may2018_concat.radiotherapyClass. 
    
    ?patientIDMon rdf:type db:infoclinical_hn_version2_30may2018_concat.patient. 
 
    ?genderMon rdf:type db:infoclinical_hn_version2_30may2018_concat.sex.
    
    ?ageMon rdf:type db:infoclinical_hn_version2_30may2018_concat.age.
    
    ?tumourMon rdf:type db:infoclinical_hn_version2_30may2018_concat.primary_site.
    
    ?hpvMon rdf:type db:infoclinical_hn_version2_30may2018_concat.hpv_status.
    
    ?followupMon rdf:type db:infoclinical_hn_version2_30may2018_concat.time_diagnosis_to_last_follow_up_days.
    
    ?tstageMon rdf:type db:infoclinical_hn_version2_30may2018_concat.t_stage.
    
    ?nstageMon rdf:type db:infoclinical_hn_version2_30may2018_concat.n_stage.
    
    ?mstageMon rdf:type db:infoclinical_hn_version2_30may2018_concat.m_stage.
    
    ?ajccMon rdf:type db:infoclinical_hn_version2_30may2018_concat.tnm_group_stage.
  
    ?surgeryMon rdf:type db:infoclinical_hn_version2_30may2018_concat.surgery.
    
    ?chemoMon rdf:type db:infoclinical_hn_version2_30may2018_concat.therapy.
 
    ?survivalMon rdf:type db:infoclinical_hn_version2_30may2018_concat.death.
        
    ?overallsurvivaldaysMon rdf:type db:infoclinical_hn_version2_30may2018_concat.time_diagnosis_to_death_days.
  
    ?regionalrecurrenceMon rdf:type db:infoclinical_hn_version2_30may2018_concat.locoregional.
    
    ?regionalrecurrencedaysMon rdf:type db:infoclinical_hn_version2_30may2018_concat.time_diagnosis_to_lr_days.
        
    ?metastasisMon rdf:type db:infoclinical_hn_version2_30may2018_concat.distant.
        
    ?metastasisdaysMon rdf:type db:infoclinical_hn_version2_30may2018_concat.time_diagnosis_to_dm_days.
 
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
addMapping("Tx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48719",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("T1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48720",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("T2", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48724",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("T3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48728",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("T4", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
# addMapping("T4b", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")

# N stage
addMapping("N0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48705",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("N1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48706",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("N2", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
# addMapping("N2b", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
# addMapping("N2c", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("N3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48714",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")

# M stage
addMapping("M0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48699",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48883")
addMapping("M1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48700",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48883")

# gender
addMapping("F", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16576",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")
addMapping("M", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C20197",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")

# survival
addMapping("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28554",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")
addMapping("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C37987",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")
# 0=alive
# 1=dead

# tumorlocation
addMapping("Oropharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping("Larynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12420",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping("Hypopharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12246",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping("Nasopharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12423",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Base of tongue", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Tonsil", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Soft palate", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
# addMapping("Glossopharyngeal sulcus", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")

# WHOstatus
# addMapping("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105722", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105721")
# addMapping("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105723", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105721")

# hpv
addMapping("%2B", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping("-", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C131488",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")

# ajcc
addMapping("stage I", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("Stade I", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("stage I", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

addMapping("Stade II", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("stage II", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("StageII", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("Stage II", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("stage IIB", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("Stage IIB", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

addMapping("stage III", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("Stade III", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("Stage III", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

addMapping("Stage IV", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("stage IV", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

addMapping("Stade IVA", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("Stage IVA", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("stage IVA", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("stage IVB", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("Stade IVB", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
# addMapping("StageIVC", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

# chemo
addMapping("chemo radiation", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
addMapping("radiation", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15313",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
# addMapping("chemo radiation", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
# addMapping("Concurrent chemoradiotherapy", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
# addMapping("Induction chemotherapy+Radiation alone", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
# addMapping("Induction chemotherapy + concurrent chemoradiotherapy", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
