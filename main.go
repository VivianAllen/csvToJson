package main

import (
	"encoding/csv"
	"encoding/json"
	"io/ioutil"
	"log"
	"os"
	"strings"

	"github.com/gosimple/slug"
)

// Metadata defines model for Metadata.
type Metadata struct {
	Code   *string `json:"code,omitempty"`
	Name   *string `json:"name,omitempty"`
	Slug   *string `json:"slug,omitempty"`
	Desc   *string `json:"desc,omitempty"`
	Tables *Tables `json:"tables,omitempty"`
}

// MetadataResponse defines model for MetadataResponse.
type MetadataResponse []Metadata

type Table struct {
	Categories *Categories `json:"categories,omitempty"`
	Code       *string     `json:"code,omitempty"`
	Name       *string     `json:"name,omitempty"`
	Slug       *string     `json:"slug,omitempty"`
	Desc       *string     `json:"desc,omitempty"`
	Total      *Triplet    `json:"total,omitempty"`
}

// Tables defines model for Tables.
type Tables []Table

// Triplet defines model for Triplet.
type Triplet struct {
	Code *string `json:"code,omitempty"`
	Name *string `json:"name,omitempty"`
	Slug *string `json:"slug,omitempty"`
}

// Categories defines model for Categories.
type Categories []Triplet

type TopicCSV struct {
	Code string
	Name string
	Desc string
}

type TableCSV struct {
	Code  string
	Name  string
	Desc  string
	Topic string
}

type CategoryCSV struct {
	Code  string
	Name  string
	Table string
}

const topicsFile = "census_atlas_metadata__-_topics_(2011_metadata).csv"
const tableFile = "census_atlas_metadata__-_tables_(2011_metadata).csv"
const catFile = "census_atlas_metadata__-_categories_(2011_metadata).csv"
const outputFile = "apiMetadata.json"

func readCsvFile(filePath string) [][]string {
	f, err := os.Open(filePath)
	if err != nil {
		log.Fatal("Unable to read input file "+filePath, err)
	}
	defer f.Close()

	csvReader := csv.NewReader(f)
	records, err := csvReader.ReadAll()
	if err != nil {
		log.Fatal("Unable to parse file as CSV for "+filePath, err)
	}

	return records
}

func parseTopicsFromCSV() []TopicCSV {
	topicsLines := readCsvFile(topicsFile)
	var topicsCSV []TopicCSV
	for _, t := range topicsLines[1:] {
		topicsCSV = append(
			topicsCSV,
			TopicCSV{
				Code: t[0],
				Name: t[1],
				Desc: t[2],
			},
		)
	}
	return topicsCSV
}

func parseTablesFromCSV() []TableCSV {
	tableLines := readCsvFile(tableFile)
	var tablesCSV []TableCSV
	for _, t := range tableLines[1:] {
		tablesCSV = append(
			tablesCSV,
			TableCSV{
				Code:  t[0],
				Name:  t[1],
				Desc:  t[2],
				Topic: t[3],
			},
		)
	}
	return tablesCSV
}

func parseCatsFromCSV() []CategoryCSV {
	catLines := readCsvFile(catFile)
	var catsCSV []CategoryCSV
	for _, t := range catLines[1:] {
		catsCSV = append(
			catsCSV,
			CategoryCSV{
				Code:  t[0],
				Name:  t[1],
				Table: t[2],
			},
		)
	}
	return catsCSV
}

func isTotalCat(catName string) bool {
	return strings.HasSuffix(catName, "0001")
}

func main() {
	topicsRaw := parseTopicsFromCSV()
	tablesRaw := parseTablesFromCSV()
	catsRaw := parseCatsFromCSV()

	// iterate through topics
	var mdr MetadataResponse

	for _, topic := range topicsRaw {
		// get matching tables
		var nestedTables Tables
		for _, table := range tablesRaw {

			if table.Topic == topic.Code {
				// get matching cats
				var nestedCats Categories
				var total Triplet

				for _, cat := range catsRaw {

					if cat.Table == table.Code {
						if isTotalCat(cat.Code) {
							total = Triplet{
								Code: spointer(cat.Code),
								Name: spointer(cat.Name),
								Slug: spointer(slug.Make(cat.Name)),
							}
						} else {
							nestedCats = append(
								nestedCats,
								Triplet{
									Code: spointer(cat.Code),
									Name: spointer(cat.Name),
									Slug: spointer(slug.Make(cat.Name)),
								},
							)
						}
					}
				}
				// append table
				nestedTables = append(
					nestedTables,
					Table{
						Categories: &nestedCats,
						Code:       spointer(table.Code),
						Name:       spointer(table.Name),
						Desc:       spointer(table.Desc),
						Slug:       spointer(slug.Make(table.Name)),
						Total:      &total,
					},
				)
			}

		}
		// append topic to mdr
		mdr = append(
			mdr,
			Metadata{
				Code:   spointer(topic.Code),
				Name:   spointer(topic.Name),
				Desc:   spointer(topic.Desc),
				Slug:   spointer(slug.Make(topic.Name)),
				Tables: &nestedTables,
			},
		)
	}
	var b []byte
	var err error
	b, err = json.Marshal(&mdr)
	if err != nil {
		panic(err)
	}
	_ = ioutil.WriteFile(outputFile, b, 0644)
}

func spointer(s string) *string {
	return &s
}
