package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
)

// Metadata defines model for Metadata.
type Metadata struct {
	Code   *string `json:"code,omitempty"`
	Name   *string `json:"name,omitempty"`
	Slug   *string `json:"slug,omitempty"`
	Tables *Tables `json:"tables,omitempty"`
}

// MetadataResponse defines model for MetadataResponse.
type MetadataResponse []Metadata

type Table struct {
	Categories *Categories `json:"categories,omitempty"`
	Code       *string     `json:"code,omitempty"`
	Name       *string     `json:"name,omitempty"`
	Slug       *string     `json:"slug,omitempty"`
}

// Tables defines model for Tables.
type Tables []Table

// Triplet defines model for Triplet.
type Quadruplet struct {
	Code *string `json:"code,omitempty"`
	Name *string `json:"name,omitempty"`
	Desc *string `json:desc,omitempty`
	Slug *string `json:"slug,omitempty"`
}

// Categories defines model for Categories.
type Categories []Quadruplet

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
	Desc  string
	Table string
}

const topicsFile = "census_atlas_metadata__-_topics.csv"
const tableFile = "census_atlas_metadata__-_tables.csv"
const catFile = "census_atlas_metadata__-_categories.csv"

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
				Desc:  t[2],
				Table: t[3],
			},
		)
	}
	return catsCSV
}

func main() {
	fmt.Println(parseTopicsFromCSV())
	fmt.Println(parseTablesFromCSV())
	fmt.Println(parseCatsFromCSV())
}
