#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

library(irr)
data <- read.csv(args[1], sep="\t")

write("\nRaw", stdout())

for (value in sort(unique(data$value))) {
  ratings <- data[data$value == value, 4:6]
  write(paste(value, kappam.fleiss(ratings)$value, sep="\t"), stdout())
}

for (i in 1:(dim(data)[1])) {
  if (data[i,]$value == "valid") {
    for (a in 4:6) {
      if (data[i,a] == 0) {
        data[data$turn_id == data[i,]$turn_id & data$model == data[i,]$model & data$value == "related",a] <- 0
        data[data$turn_id == data[i,]$turn_id & data$model == data[i,]$model & data$value == "informative",a] <- 0
        data[data$turn_id == data[i,]$turn_id & data$model == data[i,]$model & data$value == "not_generic",a] <- 0
      }
    }
  }
  if (data[i,]$value == "related") {
    for (a in 4:6) {
      if (data[i,a] == 0) {
        data[data$turn_id == data[i,]$turn_id & data$model == data[i,]$model & data$value == "informative",a] <- 0
        data[data$turn_id == data[i,]$turn_id & data$model == data[i,]$model & data$value == "not_generic",a] <- 0
      }
    }
  }
  if (data[i,]$value == "informative") {
    for (a in 4:6) {
      if (data[i,a] == 0) {
        data[data$turn_id == data[i,]$turn_id & data$model == data[i,]$model & data$value == "not_generic",a] <- 0
      }
    }
  }
}

write("\nSanitized", stdout())

for (value in sort(unique(data$value))) {
  ratings <- data[data$value == value, 4:6]
  write(paste(value, kappam.fleiss(ratings)$value, sep="\t"), stdout())
}

