#!/usr/bin/R

setwd("/home/phil/Dropbox/ODA/2018-group-projects-oda/cogyes/")

results <- read.csv("data/01_results_A_S1_done.csv")

# Remove the row with no patient ID
results <- results[-(348321),]

write.table(results, file = "data/results.tsv", sep = "\t", row.names=FALSE)
