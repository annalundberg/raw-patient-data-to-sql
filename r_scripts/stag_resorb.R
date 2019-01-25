#!/usr/bin/env R

setwd("") # set path to data directory

#load in img ids
img_id <- read.csv('data/stag_img_id.tsv')
img_id$snapshot_id <- format(img_id$snapshot_id, scientific = F)

#load in main file
stag <- read.csv('data/staging.tsv', sep = '\t')

#combine
new_stag <- cbind.data.frame(stag,img_id)
#write new file
write.table(new_stag, file = "data/staging.tsv", sep = "\t", row.names=FALSE)
