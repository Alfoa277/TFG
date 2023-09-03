library(readr)
library(car)
setwd("~/Documents/R Analysis")

dataPre <- read_delim("selectedRent.csv", 
                           delim = ";", escape_double = FALSE, col_types = cols(NEIGHBORHOOD = col_skip(), NUM_HOUSES = col_skip()
                                                                                ), trim_ws = TRUE)

dataNumFloor = data.frame(dataPre)

dataNumFloor$FLOOR[dataNumFloor$FLOOR=="UNK"] <- "-1"

dataNumFloor$FLOOR = as.integer(dataNumFloor$FLOOR)

dataNumFloor$ROOMS = as.integer(dataNumFloor$ROOMS)



cor(dataNumFloor[,c("PRICE","ROOMS","AREA","FLOOR","POPULATION")])

library(caret)

dummy = dummyVars(" ~ .",data=dataNumFloor)

new_df = data.frame(predict(dummy, newdata = dataNumFloor))

zdf <- as.data.frame(as.table(cor(new_df)))
zdf = zdf[order(zdf$Freq),]

new_df$TYPEPiso = NULL
ali =alias(lm(PRICE ~. , data = new_df), partial=TRUE)
s = ali[[2]]

delete_vars = rownames(s)

'''
IN HERE IT IS SHOWN THAT MOST OF THE PROVINCE VARIABLES ARE DELETED
 [1] "TYPEPiso"                       "PROVINCEM?laga"                 "PROVINCEMadrid"                 "PROVINCEBalears..Illes."       
 [5] "PROVINCEBarcelona"              "PROVINCELas.Palmas"             "PROVINCECantabria"              "PROVINCESalamanca"             
 [9] "PROVINCEAsturias"               "PROVINCEA.Coru?a"               "PROVINCEGranada"                "PROVINCEC?rdoba"               
[13] "PROVINCEValladolid"             "PROVINCESanta.Cruz.de.Tenerife" "PROVINCEPontevedra"             "PROVINCESevilla"               
[17] "PROVINCEGirona"                 "PROVINCEAlmer?a"                "PROVINCEToledo"                 "PROVINCENavarra"               
[21] "PROVINCEBurgos"                 "PROVINCECastell?n"              "PROVINCEAlbacete"               "PROVINCELe?n"                  
[25] "PROVINCEMurcia"                 "PROVINCETarragona"              "PROVINCEC?diz"                  "PROVINCELugo"                  
[29] "PROVINCELa.Rioja"               "PROVINCEJa?n"                   "PROVINCEAlicante"               "PROVINCEHuesca"                
[33] "PROVINCEC?ceres"                "PROVINCEBadajoz"                "PROVINCEGuadalajara" 


interesante: al ir quitando las variables de provincia, las variables de ciudad
correspondientes a la capital de provincia dejaban de tener un VIF tan alto.

LAS UNICAS REMAINING SON
[17] "PROVINCE?lava"                                  "PROVINCE?vila"                                 
 [19] "PROVINCECeuta"                                  "PROVINCECuenca"                                
 [21] "PROVINCEHuelva"                                 "PROVINCELleida"                                
 [23] "PROVINCEMelilla"                                "PROVINCEOurense"                               
 [25] "PROVINCEPalencia"                               "PROVINCESegovia"                               
 [27] "PROVINCESoria"                                  "PROVINCETeruel"                                
 [29] "PROVINCEZamora"
 
 
 
Todas las borradas son
   [1] "TYPETorre"                                       "PROVINCEZaragoza"                               
 [3] "TOWNceuta"                                       "TOWNlleida"                                     
 [5] "TOWNmelilla"                                     "TOWNnavaluenga"                                 
 [7] "TOWNourense"                                     "TOWNpalencia"                                   
 [9] "TOWNpuente.genil"                                "TOWNpunta.umbria"                               
[11] "TOWNsegovia"                                     "TOWNsojuela"                                    
[13] "TOWNsoria"                                       "TOWNtarancon"                                   
[15] "TOWNteo"                                         "TOWNteruel"                                     
[17] "TOWNtorre.pacheco"                               "TOWNtorrenueva.costa"                           
[19] "TOWNtorrevieja"                                  "TOWNtortosa"                                    
[21] "TOWNtossa.de.mar"                                "TOWNtrujillo"                                   
[23] "TOWNtudela"                                      "TOWNutrera"                                     
[25] "TOWNvalldemossa"                                 "TOWNvalverde"                                   
[27] "TOWNvicar"                                       "TOWNvilagarcia.de.arousa"                       
[29] "TOWNvilassar.de.mar"                             "TOWNvillacarrillo"                              
[31] "TOWNvillanua"                                    "TOWNvillaquilambre"                             
[33] "TOWNvillarcayo.de.merindad.de.castilla.la.vieja" "TOWNvillares.de.la.reina"                       
[35] "TOWNvillarrobledo"                               "TOWNvillaviciosa"                               
[37] "TOWNvillaviciosa.de.odon"                        "TOWNvinaros"                                    
[39] "TOWNvitoria.gasteiz"                             "TOWNvoto"                                       
[41] "TOWNxove"                                        "TOWNyaiza"                                      
[43] "TOWNyebes"                                       "TOWNyuncos"                                     
[45] "TOWNzafra"                                       "TOWNzahara.de.los.atunes"                       
[47] "TOWNzamora"                                      "TOWNzaratan"                                    
[49] "TOWNzuera"                                       "LOCATIONUNK"                                    
[51] "ELEVATORUNK"                                     "GARAGETRUE"                                     
[53] "TYPEPiso"                                        "PROVINCEM?laga"                                 
[55] "PROVINCEMadrid"                                  "PROVINCEBalears..Illes."                        
[57] "PROVINCEBarcelona"                               "PROVINCELas.Palmas"                             
[59] "PROVINCECantabria"                               "PROVINCESalamanca"                              
[61] "PROVINCEAsturias"                                "PROVINCEA.Coru?a"                               
[63] "PROVINCEGranada"                                 "PROVINCEC?rdoba"                                
[65] "PROVINCEValladolid"                              "PROVINCESanta.Cruz.de.Tenerife"                 
[67] "PROVINCEPontevedra"                              "PROVINCESevilla"                                
[69] "PROVINCEGirona"                                  "PROVINCEAlmer?a"                                
[71] "PROVINCEToledo"                                  "PROVINCENavarra"                                
[73] "PROVINCEBurgos"                                  "PROVINCECastell?n"                              
[75] "PROVINCEAlbacete"                                "PROVINCELe?n"                                   
[77] "PROVINCEMurcia"                                  "PROVINCETarragona"                              
[79] "PROVINCEC?diz"                                   "PROVINCELugo"                                   
[81] "PROVINCELa.Rioja"                                "PROVINCEJa?n"                                   
[83] "PROVINCEAlicante"                                "PROVINCEHuesca"                                 
[85] "PROVINCEC?ceres"                                 "PROVINCEBadajoz"                                
[87] "ELEVATORTrue"                                    "PROVINCEGuadalajara" 
 '''

new_data = new_df[, !names(new_df) %in% delete_vars]
ali =alias(lm(PRICE ~. , data = new_data),partial=TRUE)

model <- lm(PRICE ~. , data = new_data)

summary(model)


vif_df = vif(model)

vif_df[order(vif_df)]


deteled_vars = c(delete_vars)
r_squared = c()
adjusted_rsquared = c()
condition = TRUE

while(condition){
  new_data = new_df[, !names(new_df) %in% deteled_vars]
  model <- lm(PRICE ~. , data = new_data)
  vif_df = vif(model)
  vif_df = vif_df[order(vif_df)]
  summar = summary(model)
  print(vif_df[(length(vif_df)-3):length(vif_df)])
  r_squared=c(r_squared, summar$r.squared)
  adjusted_rsquared = c(adjusted_rsquared, summar$adj.r.squared)
  control = vif_df[length(vif_df)]
  if(control>10){
    deteled_vars=c(deteled_vars,names(control))
  } else {
    condition=FALSE
  }
}

write.csv(new_data,"dataSelected.csv",row.names = FALSE)

##### SOLD ####
soldPre <- read_delim("soldPre.csv", delim = ";", 
                      escape_double = FALSE, col_types = cols(...1 = col_skip()), 
                      trim_ws = TRUE)
soldPre = data.frame(soldPre)

soldPre$FLOOR[soldPre$FLOOR=="UNK"] <- "-1"

soldPre$FLOOR = as.integer(soldPre$FLOOR)

dummy = dummyVars(" ~ .",data=soldPre)

new_sold = data.frame(predict(dummy, newdata = soldPre))
new_sold = new_sold[, !names(new_sold) %in% deteled_vars]
write.csv(new_sold,"soldSelected.csv",row.names = FALSE)


save(deteled_vars,model,file = 'deletedvars.Rdata')


########

delete = c("TYPETorre","PROVINCEZaragoza"                               
,"TOWNceuta","TOWNlleida"                                     
,"TOWNmelilla","TOWNnavaluenga"                                 
,"TOWNourense","TOWNpalencia"                                   
,"TOWNpuente.genil","TOWNpunta.umbria"                               
,"TOWNsegovia","TOWNsojuela"                                    
,"TOWNsoria","TOWNtarancon"                                   
,"TOWNteo","TOWNteruel"                                     
,"TOWNtorre.pacheco","TOWNtorrenueva.costa"                           
,"TOWNtorrevieja","TOWNtortosa"                                    
,"TOWNtossa.de.mar","TOWNtrujillo"                                   
   ,"TOWNtudela","TOWNutrera"                                     
,"TOWNvalldemossa","TOWNvalverde"                                   
,"TOWNvicar","TOWNvilagarcia.de.arousa"                       
,"TOWNvilassar.de.mar","TOWNvillacarrillo"                              
,"TOWNvillanua", "TOWNvillaquilambre"                             
,"TOWNvillarcayo.de.merindad.de.castilla.la.vieja","TOWNvillares.de.la.reina"                       
,"TOWNvillarrobledo","TOWNvillaviciosa"                               
,"TOWNvillaviciosa.de.odon","TOWNvinaros"                                    
 ,"TOWNvitoria.gasteiz","TOWNvoto"                                       
,"TOWNxove","TOWNyaiza"                                      
,"TOWNyebes","TOWNyuncos"                                     
,"TOWNzafra","TOWNzahara.de.los.atunes"                       
, "TOWNzamora","TOWNzaratan"                                    
,"TOWNzuera","LOCATIONUNK"                                    
,"ELEVATORUNK","GARAGETRUE"                                     
, "TYPEPiso","PROVINCEMálaga"                                 
,"PROVINCEMadrid","PROVINCEBalears..Illes."                        
,"PROVINCEBarcelona","PROVINCELas.Palmas"                             
,"PROVINCECantabria","PROVINCESalamanca"                              
,"PROVINCEAsturias","PROVINCEA.Coruña"                               
,"PROVINCEGranada","PROVINCECórdoba"                                
,"PROVINCEValladolid","PROVINCESanta.Cruz.de.Tenerife"                 
, "PROVINCEPontevedra","PROVINCESevilla"                                
,"PROVINCEGirona","PROVINCEAlmería"                                
,"PROVINCEToledo","PROVINCENavarra"                                
,"PROVINCEBurgos","PROVINCECastellón"                              
,"PROVINCEAlbacete","PROVINCELeón"                                   
,"PROVINCEMurcia","PROVINCETarragona"                              
,"PROVINCECádiz","PROVINCELugo"                                   
,"PROVINCELa.Rioja","PROVINCEJaén"                                   
,"PROVINCEAlicante","PROVINCEHuesca"                                 
,"PROVINCECáceres","PROVINCEBadajoz"                                
,"ELEVATORTrue","PROVINCEGuadalajara")

new_data = new_df[, !names(new_df) %in% delete]
write.csv(new_data,"rentPost.csv",row.names = FALSE)
