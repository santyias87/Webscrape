install.packages("foreign")
install.packages ("rvest")
install.packages("dplyr")
library(foreign)
library(rvest)
library(dplyr)

df<-read.csv("D:/Data_Science/Webscrape/restaurants_sorted2.csv")
v1 <- df$Data_ID
v2 <- df$Distance
v3 <- df$Duplicate

i <- 1

for (val in v1) {
  ind <- which (v1 %in% val)
  if( min(v2[ind]) == v2[i])  {
    v3[i] <- "TRUE"
    } else {
    v3[i] <- "FALSE"}
  i <- i +1
}
df$Duplicate <- v3

length(which(v3 %in% FALSE))
length(df)

df2 <- df %>% filter(Duplicate == TRUE)

  
write.csv(df2, "D:/Data_Science/Webscrape/restaurants_cleaned.csv")
