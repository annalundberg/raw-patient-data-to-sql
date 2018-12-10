#!/usr/bin/R

##set directory containing data
setwd("<path_to_datafiles>")

results <- read.csv("data/01_results_A_S1_done.csv")

## Remove the row with no patient ID ##
results <- results[-(348321),]

write.table(results, file = "data/results.tsv", sep = "\t", row.names=FALSE)
