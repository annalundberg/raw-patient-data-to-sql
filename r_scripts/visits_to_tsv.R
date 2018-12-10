#!/usr/bin/env R

setwd("~/bgmp/oda/2018-group-projects-oda/cogyes/")

results <- read.csv("data/Visits.csv")

write.table(results, file = "data/visits.tsv", sep = "\t", row.names=FALSE)
