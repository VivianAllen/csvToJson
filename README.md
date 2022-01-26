# Intro

Utility functions to convert csv with census metadata, downloaded from google sheets, into a .json file suitable for consumption by the atlas.

# Downloading data

New/updated metadata will be added to this sheet: https://docs.google.com/spreadsheets/d/1Q0Sckm8ss2gwTa4SROprYkKRQ1NJ-5MBzRiCiAFYUeE/edit#gid=1217010592

The tabs that should be downloaded as csv (**in menu, file->download->csv with the tab you want to download open**) are:
- [topics](https://docs.google.com/spreadsheets/d/1Q0Sckm8ss2gwTa4SROprYkKRQ1NJ-5MBzRiCiAFYUeE/edit#gid=0)
- [tables](https://docs.google.com/spreadsheets/d/1Q0Sckm8ss2gwTa4SROprYkKRQ1NJ-5MBzRiCiAFYUeE/edit#gid=1217010592)
- [categories](https://docs.google.com/spreadsheets/d/1Q0Sckm8ss2gwTa4SROprYkKRQ1NJ-5MBzRiCiAFYUeE/edit#gid=1758829387)

Once downloaded as csv and placed in the root folder of this project, run `./rename-gsheets-csv.sh` to normalise the file names for consumption by the Go conversion script.

# Converting to JSON

Once all three files have been renamed with `./rename-gsheets-csv.sh`, run `go run main.go` to produce the `apiMetadata.json` file. 

# Workarounds / Tweaks

There are currently some tables with missing data - `KS207WA` and `KS208WA`. The entries for these in the `tables` array under the topic `Identity` should deleted from `apiMetadata.json`

# Submitting PR to atlas FE

- clone the [FE repo](https://github.com/ONSdigital/census-atlas) from git@github.com:ONSdigital/census-atlas.git
- make a branch
- copy the contents of `apiMetadata.json` into the exported default object in [src/data/apiMetadata.js](https://github.com/ONSdigital/census-atlas/blob/master/src/data/apiMetadata.js)
- check in etc and submit PR to change contents of `src/data/apiMetadata.js`


# Misc

If you need to convert [existing metadata from the geodata api](http://ec2-18-193-78-190.eu-central-1.compute.amazonaws.com:25252/metadata/2011) into csv form suitable for loading into google sheets for manual editing, the python script `metaToCsv.py` can be used. This is Python 3.9 and does not use any non-standard-library packages, so as long as you have python 3.9 you should just be able to run it. This will produce three csv files from the output of the geodata API metadata endpoint:
- original_categories.csv
- original_tables.csv
- original_topics.csv