#!/usr/bin/env R

setwd("~/bgmp/oda/2018-group-projects-oda/cogyes/")

hospital <- read.csv("data/Hospitalizations.csv")
hosp1 <- hospital[1:2]
hosp2 <- hospital[4:7]
new_hosp <- cbind.data.frame(hosp1,hosp2)

write.table(new_hosp, file = "data/hospital.tsv", sep = "\t", row.names=FALSE)
