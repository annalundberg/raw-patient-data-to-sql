#!/usr/bin/env R

##set directory containing data
setwd("<path_to_datafiles>")

results <- read.csv("data/Visits.csv")

write.table(results, file = "data/visits.tsv", sep = "\t", row.names=FALSE)
