library(tidyverse)
library(readr)
library(tibble)


### ONLY CHANGE PARAMETERS HERE, DON'T CHANGE ANYTHING ELSE ###
setwd("H:/MAIN Project Files/AAA DEVELOPMENT PROJECTS/000 DEVELOPMENT RESOURCES/CA/California Search Lists/SCE Q1 24/Tier 2 Exports") #Folder with a utility's csvs must use / NOT \ in filepaths
file_list <- list.files(pattern = "Q124") # %>% Only change what's between " " that's your search cursor. Smart to do county
#  lapply(read_csv) #can ignore, line is for other uses
filename <- "AO CA Search FO (q124) PG&E Tier 2.csv" # Sets your filename only change " " and leave extension as .csv use two digit state abbrev, ## to group, COUNTY to county, # to tier number
tier <- "Tier 2" #change to whatever tier you're doing
utility <- "PG&E" #change to utility name as you want it displayed in final sheet
market <- "CA" #market you're in as two character abbrev
status <- "Open" #status of leads
Star1 <- "N/A"
Star2 <- "LMI"
Star3 <- "EC/CC"
### NO MORE CHANGING ###

refactor <- map_dfr(.x = set_names(file_list),
                  .f = ~ read_csv(.x, col_types = cols(.default = "c",`Zip (Mailing Address)`="c", `Star Rating`="c")))

### refactor function if necessary ###
#func <- function(data, my_col){
#  my_col <-enexpr(my_col)
  
#  output <- data %>%
#    mutate(!!my_col := as.numeric(!!my_col))
#}

merged <- dplyr::bind_rows(refactor)

renamed <- merged %>% 
  rename (
    `Site County` = County,
    `AO Link` = `Asset Url`,
    `IRA Status` = `Star Rating`,
    `Robust ID` = `Robust Id (Reportall)`
  )
add <- renamed %>% 
  add_column(Email = NA,
             Group = NA,
             `Site #` = NA,
             `Site Tier` = tier,
             Utility = utility,
             Market = market,
             `Lead Status` = status,
             `Zip/Postal Code` = NA,
             Phone = NA,
             `Other Phone` = NA,
             `Mobile` = NA,
             `Site Lat/Long` = paste(renamed$Latitude,renamed$Longitude,sep=";")
             )

#for yes phone numbers no coords#colOrder <- c('First Name','Last Name','Company','Site Address','Site City','Site State','Site Zip Code','APN/PIN','Site Municipal','Site County','Buildable Area (Acres)','Lot Size','Street','Address Line 2','City (Mailing Address)','State (Mailing Address)','Zip (Mailing Address)','Phone','Other Phone','Mobile','Phone 1 (Site Address)','Phone 2 (Site Address)','Phone 3 (Site Address)','Phone 1 (Mailing Address)','Phone 2 (Mailing Address)','Phone 3 (Mailing Address)','Email','AO Project','Group','Site #','AO Link','Site Tier','Utility','Market','Lead Status','IRA Status')
#preserve data colOrder <- c('First Name','Last Name','Company','Site Address','Site City','Site State','Site Zip Code','APN/PIN','Site Municipal','Site County','Lot Size','Street','Address Line 2','City','State','Zip/Postal Code','City (Mailing Address)','State (Mailing Address)','Zip (Mailing Address)','Phone','Other Phone','Mobile','Phone 1 (Site Address)','Phone 2 (Site Address)','Phone 3 (Site Address)','Phone 1 (Mailing Address)','Phone 2 (Mailing Address)','Phone 3 (Mailing Address)','Email','AO Project','Group','Site #','AO Link','Site Tier','Utility','Market','Lead Status','IRA Status')
#for yes phone numbers, yes coords#colOrder <- c('First Name','Last Name','Company','Site Address','Site City','Site State','Site Zip Code','APN/PIN','Site Municipal','Site County','Lot Size','Street','Address Line 2','City (Mailing Address)','State (Mailing Address)','Zip (Mailing Address)','Phone','Other Phone','Mobile','Phone 1 (Site Address)','Phone 2 (Site Address)','Phone 3 (Site Address)','Phone 1 (Mailing Address)','Phone 2 (Mailing Address)','Phone 3 (Mailing Address)','Email','AO Project','Group','Site #','AO Link','Site Tier','Utility','Market','Lead Status','IRA Status','Site Lat/Long', 'Robust ID')
colOrder <- c('First Name','Last Name','Company','Site Address','Site City','Site State','Site Zip Code','APN/PIN','Site Municipal','Site County','Buildable Area (Acres) (acre)','Lot Size (acre)','Street','Address Line 2','City (Mailing Address)','State (Mailing Address)','Zip (Mailing Address)','Phone','Other Phone','Mobile','Email','AO Project','Group','Site #','AO Link','Site Tier','Utility','Market','Lead Status','IRA Status','Site Lat/Long', 'Robust ID')

ordered <- add[, colOrder]

#ordered["IRA Status"][ordered["IRA Status"] == "2"] <- "No"
#ordered["IRA Status"][ordered["IRA Status"] == "3"] <- "Yes"

ordered["IRA Status"][ordered["IRA Status"] == "1"] <- Star1
ordered["IRA Status"][ordered["IRA Status"] == "2"] <- Star2
ordered["IRA Status"][ordered["IRA Status"] == "3"] <- Star3

renamed2 <- ordered %>%
  rename (
  City = `City (Mailing Address)`,
  State = `State (Mailing Address)`,
  `Zip/Postal Code` = `Zip (Mailing Address)`,
  `Buildable Area (Acres)` = `Buildable Area (Acres) (acre)`,
  `Lot Size` = `Lot Size (acre)`
)
renamed2$`Zip/Postal Code` <- substr(renamed2$`Zip/Postal Code`, 0, 5)

write.csv(renamed2, filename)
