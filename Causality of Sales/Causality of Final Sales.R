###Code in Causality of Final Sales 

##Using Excel, we transform the Creation date format to Month-Year
jdquote1 = read.csv("jdquote1.csv")
##After joining two tables together, we deleted all columns/variables that intutively are not relevant in analysis on quote table
jdquote2 = jdquote1[c("QuoteType", "CreationDate",          
                      "ExpirationDate", "CurrentQuoteStatus", "SalesPersonName","StateProvince",           
                      "DealerID","DealerCity","DealerState","EquipmentType",           
                      "EquipmentAmount","SellingPrice","EquipmentManufacturer","EquipmentCategoryDesc",   
                      "EquipmentSubCategoryDesc","EquipmentStatus","FinanceIncentive","TradeDifference",
                      "Net.Cost","WorkFlow.Status","Base.Implement","CustomerName"),]

##After identify key variables, then we deleted all null value that will affect our analysis because it is not appropriate to replace null values with information from other records.
jdquote3=jdquote2[!is.null(jdquote2$quoteType) |is.null(jdquote2$quoteType)|is.null(jdquote2$QuoteType)|is.null(jdquote2$CreationDate)|is.null(jdquote2$CurrentQuoteStatus)|is.null(jdquote2$DealerCity)|is.null(jdquote2$EquipmentType)|is.null(jdquote2$Base.Implement)|is.null(jdquote2$WorkFlow.Status)|is.null(jdquote2$EquipmentStatus)]


jdquote5=read.csv("jdquote5.csv",head = T)

##Then we add quote Status that can be related to the joint table to the cleaned quote table as 1, else the status is 0.
for (i in 1:nrow(jdquote5)){
  if (jdquote5['X'][i,1] %in% jointtable['X'][,1]){
    jdquote5['Status1'][i,1] = 1
  }
  
}

for (i in 1:nrow(jdquote5)){
  if (jdquote5['EquipmentStatus'][i,1] == 'Used'){
    jdquote5['epstatus'][i,1] = 'Used'}
}

##Finally, we generate the best models using logistic model
glm1=glm(factor(Status)~as.factor(QuoteType)+as.factor(CreationDate)+as.factor(QuoteType)+as.factor(CurrentQuoteStatus)+as.factor(DealerCity)+as.factor(EquipmentType)+as.factor(Base.Implement)+as.factor(WorkFlow.Status)+as.factor(epstatus)+SellingPrice,family=binomial(link='logit'),data=jdquote5)
summary(glm1)