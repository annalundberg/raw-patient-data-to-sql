#!/usr/bin/env R

setwd("") # set path to data directory

stag <- read.csv("data/orig_data/Staging.csv")

stag1 <- stag[1:25]
stag2 <- stag[27:38]
new_stag <- cbind.data.frame(stag1,stag2)

write.table(new_stag, file = "data/staging.tsv", sep = "\t", row.names=FALSE)
write.table(stag[26], file = 'data/stag_link.tsv', sep = '\t', row.names=FALSE)
