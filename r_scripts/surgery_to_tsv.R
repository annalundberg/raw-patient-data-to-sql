#!/usr/bin/env R

##set directory containing data
setwd("<path_to_datafiles>")

## remove blank column ##
surgery <- read.csv("data/Surgery.csv")
surg1 <- surgery[1:2]
surg2 <- surgery[4:22]
new_surg <- cbind.data.frame(surg1,surg2)

write.table(new_surg, file = "data/surgery.tsv", sep = "\t", row.names=FALSE)
