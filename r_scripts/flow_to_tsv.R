#!/usr/bin/R

##set directory containing data
setwd("<path_to_datafiles>")

results <- read.csv("data/02_flowsheet_AB_S1_done.csv")

write.table(results, file = "data/flow.tsv", sep = "\t", row.names=FALSE)
