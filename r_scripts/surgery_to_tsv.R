#!/usr/bin/env R

setwd("~/bgmp/oda/2018-group-projects-oda/cogyes/")

surgery <- read.csv("data/Surgery.csv")
surg1 <- surgery[1:2]
surg2 <- surgery[4:22]
new_surg <- cbind.data.frame(surg1,surg2)

write.table(new_surg, file = "data/surgery.tsv", sep = "\t", row.names=FALSE)
