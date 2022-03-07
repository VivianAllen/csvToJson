import csv
import json
import pathlib
import shutil
import tempfile

from unittest import TestCase

import csv_to_meta

class TestCsvToMeta(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_fp = pathlib.PurePath(self.test_dir.name, 'test.csv')

    def tearDown(self):
        shutil.rmtree(self.test_dir.name)

    def write_test_CSV(self, csvRowList):
        with open(self.test_fp, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(csvRowList)

    def read_test_JSON(self):
        with open(self.test_fp.with_suffix(".apiMetadata.json"), 'r') as f:
            json_contents = json.load(f)
        return json_contents

    def test_content_csv_to_json_OK_no_subcategories(self):
        # GIVEN we have written a csv with one topic and two tables, each with three categories and one total
        self.write_test_CSV([
            ["name","desc","class","nomis_code","nomis_units"],
            ["Test Topic", "topic desc", "topic", ""],
            ["Test Table 1", "table 1 desc", "table", "test_table_1_code", ""],
            ["Test Category 1 Total", "", "category", "test_category_1_0001", "Person"],
            ["Test Category 1_1", "", "category", "test_category_1_1_code", "Person"],
            ["Test Category 2_1", "","category", "test_category_2_1_code", "Person"],
            ["Test Category 3_1", "","category", "test_category_3_1_code", "Person"],
            ["Test Table 2", "table 2 desc", "table", "test_table_2_code", ""],
            ["Test Category 2 Total", "", "category", "test_category_2_0001", "Households"],
            ["Test Category 1_2", "", "category", "test_category_1_2_code", "Households"],
            ["Test Category 2_2", "", "category", "test_category_2_2_code", "Households"],
            ["Test Category 3_2", "", "category", "test_category_3_2_code", "Households"],
        ])
       
        # WHEN we call the main function of csv_to_meta
        csv_to_meta.main(self.test_fp)

        # THEN we expect to get a properly formatted JSON back
        expected = [
                {
                    "code": "Test Topic",
                    "name": "Test Topic",
                    "slug": "test-topic",
                    "desc": "topic desc",
                    "tables": [
                        {
                            "code": "test_table_1_code",
                            "name": "Test Table 1",
                            "slug": "test-table-1",
                            "desc": "table 1 desc",
                            "units": "People", # NB - this is transformed from 'People', bit awkward, should be removed ASAP
                            "total": {
                                "code": "test_category_1_0001",
                                "name": "Test Category 1 Total",
                                "slug": "test-category-1-total"
                            },
                            "categories": [
                                {
                                    "code": "test_category_1_1_code",
                                    "name": "Test Category 1_1",
                                    "slug": "test-category-1-1"
                                },
                                {
                                    "code": "test_category_2_1_code",
                                    "name": "Test Category 2_1",
                                    "slug": "test-category-2-1"
                                },
                                {
                                    "code": "test_category_3_1_code",
                                    "name": "Test Category 3_1",
                                    "slug": "test-category-3-1"
                                },
                            ]
                        },
                        {
                            "code": "test_table_2_code",
                            "name": "Test Table 2",
                            "slug": "test-table-2",
                            "desc": "table 2 desc",
                            "units": "Households",
                            "total": {
                                "code": "test_category_2_0001",
                                "name": "Test Category 2 Total",
                                "slug": "test-category-2-total"
                            },
                            "categories": [
                                {
                                    "code": "test_category_1_2_code",
                                    "name": "Test Category 1_2",
                                    "slug": "test-category-1-2"
                                },
                                {
                                    "code": "test_category_2_2_code",
                                    "name": "Test Category 2_2",
                                    "slug": "test-category-2-2"
                                },
                                {
                                    "code": "test_category_3_2_code",
                                    "name": "Test Category 3_2",
                                    "slug": "test-category-3-2"
                                },
                            ]
                        }
                    ]
                }
        ]
        returned = self.read_test_JSON()
        self.assertEqual(expected, returned)

    def test_content_csv_to_json_OK_subcategories(self):
        # GIVEN we have written a csv with one topic and two tables, each with three categories and one total
        # and one with three subcategories
        self.write_test_CSV([
            ["name","desc","class","nomis_code","nomis_units"],
            ["Test Topic", "topic desc", "topic", ""],
            ["Test Table 1", "table 1 desc", "table", "test_table_1_code", ""],
            ["Test Category 1 Total", "", "category", "test_category_1_0001", "Person"],
            ["Test Category 1_1", "", "category", "test_category_1_1_code", "Person"],
            ["Test Category 2_1", "","category", "test_category_2_1_code", "Person"],
            ["Test Category 2_1_1", "","sub-category", "test_category_2_1_1_code", "Person"],
            ["Test Category 2_1_2", "","sub-category", "test_category_2_1_2_code", "Person"],
            ["Test Category 2_1_3", "","sub-category", "test_category_2_1_3_code", "Person"],
            ["Test Category 3_1", "","category", "test_category_3_1_code", "Person"],
            ["Test Table 2", "table 2 desc", "table", "test_table_2_code", ""],
            ["Test Category 2 Total", "", "category", "test_category_2_0001", "Households"],
            ["Test Category 1_2", "", "category", "test_category_1_2_code", "Households"],
            ["Test Category 2_2", "", "category", "test_category_2_2_code", "Households"],
            ["Test Category 3_2", "", "category", "test_category_3_2_code", "Households"],
        ])
       
        # WHEN we call the main function of csv_to_meta
        csv_to_meta.main(self.test_fp)

        # THEN we expect to get a properly formatted JSON back
        expected = [
                {
                    "code": "Test Topic",
                    "name": "Test Topic",
                    "slug": "test-topic",
                    "desc": "topic desc",
                    "tables": [
                        {
                            "code": "test_table_1_code",
                            "name": "Test Table 1",
                            "slug": "test-table-1",
                            "desc": "table 1 desc",
                            "units": "People", # NB - this is transformed from 'People', bit awkward, should be removed ASAP
                            "total": {
                                "code": "test_category_1_0001",
                                "name": "Test Category 1 Total",
                                "slug": "test-category-1-total"
                            },
                            "categories": [
                                {
                                    "code": "test_category_1_1_code",
                                    "name": "Test Category 1_1",
                                    "slug": "test-category-1-1"
                                },
                                {
                                    "code": "test_category_2_1_code",
                                    "name": "Test Category 2_1",
                                    "slug": "test-category-2-1",
                                    "sub-categories": [
                                        {
                                            "code": "test_category_2_1_1_code",
                                            "name": "Test Category 2_1_1",
                                            "slug": "test-category-2-1-1"
                                        },
                                        {
                                            "code": "test_category_2_1_2_code",
                                            "name": "Test Category 2_1_2",
                                            "slug": "test-category-2-1-2"
                                        },
                                        {
                                            "code": "test_category_2_1_3_code",
                                            "name": "Test Category 2_1_3",
                                            "slug": "test-category-2-1-3"
                                        },
                                    ]
                                },
                                {
                                    "code": "test_category_3_1_code",
                                    "name": "Test Category 3_1",
                                    "slug": "test-category-3-1"
                                },
                            ]
                        },
                        {
                            "code": "test_table_2_code",
                            "name": "Test Table 2",
                            "slug": "test-table-2",
                            "desc": "table 2 desc",
                            "units": "Households",
                            "total": {
                                "code": "test_category_2_0001",
                                "name": "Test Category 2 Total",
                                "slug": "test-category-2-total"
                            },
                            "categories": [
                                {
                                    "code": "test_category_1_2_code",
                                    "name": "Test Category 1_2",
                                    "slug": "test-category-1-2"
                                },
                                {
                                    "code": "test_category_2_2_code",
                                    "name": "Test Category 2_2",
                                    "slug": "test-category-2-2"
                                },
                                {
                                    "code": "test_category_3_2_code",
                                    "name": "Test Category 3_2",
                                    "slug": "test-category-3-2"
                                },
                            ]
                        }
                    ]
                }
        ]
        returned = self.read_test_JSON()
        self.assertEqual(expected, returned)
