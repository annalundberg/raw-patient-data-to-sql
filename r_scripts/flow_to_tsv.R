#!/usr/bin/R

setwd("/home/phil/Dropbox/ODA/2018-group-projects-oda/cogyes/")

results <- read.csv("data/02_flowsheet_AB_S1_done.csv")

write.table(results, file = "data/flow.tsv", sep = "\t", row.names=FALSE)
