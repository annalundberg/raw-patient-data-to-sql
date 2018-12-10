#!/usr/bin/env R

##set directory containing data
setwd("<path_to_datafiles>")

hospital <- read.csv("data/Hospitalizations.csv")

## slice out illogical age column ##
hosp1 <- hospital[1:2]
hosp2 <- hospital[4:7]
new_hosp <- cbind.data.frame(hosp1,hosp2)

write.table(new_hosp, file = "data/hospital.tsv", sep = "\t", row.names=FALSE)
