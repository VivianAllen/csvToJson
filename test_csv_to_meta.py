import csv
import json
import os
import pathlib
import shutil
import tempfile

from unittest import TestCase

from csv_to_meta import DESC_PLACEHOLDER


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

    def test_content_csv_to_json_OK_one_topic_no_subcategories(self):
        # GIVEN we have written a csv with one topic and two tables, each with three categories and one total
        self.write_test_CSV([
            ["name","desc","taxonomy","code","units"],
            ["Topic 1", "topic desc.", "topic", "", ""],
            ["Classification 1", "Classification 1 desc.", "classification", "classification_1_code", "units_1"],
            ["Category 1 Total", "Category 1 Total desc.", "category", "category_1_0001", ""],
            ["Category 1_1", "Category 1_1 desc.", "category", "category_1_1_code", ""],
            ["Category 2_1", "Category 2_1 desc.","category", "category_2_1_code", ""],
            ["Category 3_1", "Category 3_1 desc.","category", "category_3_1_code", ""],
            ["Classification 2", "Classification 2 desc.", "classification", "classification_2_code", "units_2"],
            ["Category 2 Total", "Category 2 Total desc.", "category", "category_2_0001", ""],
            ["Category 2_1", "Category 2_1 desc.", "category", "category_2_1_code", ""],
            ["Category 2_2", "Category 2_2 desc.", "category", "category_2_2_code", ""],
            ["Category 2_3", "Category 2_3 desc.", "category", "category_2_3_code", ""],
        ])
       
        # WHEN we run the csv_to_meta script
        os.system(f"python csv_to_meta.py {self.test_fp}")

        # THEN we expect to get a properly formatted JSON back
        expected = [
            {
                "code": "Topic 1",
                "name": "Topic 1",
                "slug": "topic-1",
                "desc": "topic desc.",
                "classifications": [
                    {
                        "code": "classification_1_code",
                        "name": "Classification 1",
                        "slug": "classification-1",
                        "desc": "Classification 1 desc.",
                        "units": "units_1",
                        "total": {
                            "code": "category_1_0001",
                            "name": "Category 1 Total",
                            "slug": "category-1-total",
                            "desc": "Category 1 Total desc."
                        },
                        "categories": [
                            {
                                "code": "category_1_1_code",
                                "name": "Category 1_1",
                                "slug": "category-1-1",
                                "desc": "Category 1_1 desc."
                            },
                            {
                                "code": "category_2_1_code",
                                "name": "Category 2_1",
                                "slug": "category-2-1",
                                "desc": "Category 2_1 desc."
                            },
                            {
                                "code": "category_3_1_code",
                                "name": "Category 3_1",
                                "slug": "category-3-1",
                                "desc": "Category 3_1 desc."
                            },
                        ]
                    },
                    {
                        "code": "classification_2_code",
                        "name": "Classification 2",
                        "slug": "classification-2",
                        "desc": "Classification 2 desc.",
                        "units": "units_2",
                        "total": {
                            "code": "category_2_0001",
                            "name": "Category 2 Total",
                            "slug": "category-2-total",
                            "desc": "Category 2 Total desc."
                        },
                        "categories": [
                            {
                                "code": "category_2_1_code",
                                "name": "Category 2_1",
                                "slug": "category-2-1",
                                "desc": "Category 2_1 desc."
                            },
                            {
                                "code": "category_2_2_code",
                                "name": "Category 2_2",
                                "slug": "category-2-2",
                                "desc": "Category 2_2 desc."
                            },
                            {
                                "code": "category_2_3_code",
                                "name": "Category 2_3",
                                "slug": "category-2-3",
                                "desc": "Category 2_3 desc."
                            },
                        ]
                    },
                ]
            }
        ]
        returned = self.read_test_JSON()
        self.assertEqual(expected, returned)

    def test_content_csv_to_json_OK_subcategories(self):
        # GIVEN we have written a csv with one topic and two tables, each with three categories and one total
        # and one with one category with three subcategories
        self.write_test_CSV([
            ["name","desc","taxonomy","code","units"],
            ["Topic 1", "topic desc.", "topic", "", ""],
            ["Classification 1", "Classification 1 desc.", "classification", "classification_1_code", "units_1"],
            ["Category 1 Total", "Category 1 Total desc.", "category", "category_1_0001", ""],
            ["Category 1_1", "Category 1_1 desc.", "category", "category_1_1_code", ""],
            ["Category 2_1", "Category 2_1 desc.","category", "category_2_1_code", ""],
            ["Sub-category 2_1_1", "Sub-category 2_1_1 desc.","sub-category", "sub-category_2_1_1_code", ""],
            ["Sub-category 2_1_2", "Sub-category 2_1_2 desc.","sub-category", "sub-category_2_1_2_code", ""],
            ["Sub-category 2_1_3", "Sub-category 2_1_3 desc.","sub-category", "sub-category_2_1_3_code", ""],
            ["Category 3_1", "Category 3_1 desc.","category", "category_3_1_code", ""],
            ["Classification 2", "Classification 2 desc.", "classification", "classification_2_code", "units_2"],
            ["Category 2 Total", "Category 2 Total desc.", "category", "category_2_0001", ""],
            ["Category 2_1", "Category 2_1 desc.", "category", "category_2_1_code", ""],
            ["Category 2_2", "Category 2_2 desc.", "category", "category_2_2_code", ""],
            ["Category 2_3", "Category 2_3 desc.", "category", "category_2_3_code", ""],
        ])
       
        # WHEN we run the csv_to_meta script
        os.system(f"python csv_to_meta.py {self.test_fp}")

        # THEN we expect to get a properly formatted JSON back
        expected = [
            {
                "code": "Topic 1",
                "name": "Topic 1",
                "slug": "topic-1",
                "desc": "topic desc.",
                "classifications": [
                    {
                        "code": "classification_1_code",
                        "name": "Classification 1",
                        "slug": "classification-1",
                        "desc": "Classification 1 desc.",
                        "units": "units_1",
                        "total": {
                            "code": "category_1_0001",
                            "name": "Category 1 Total",
                            "slug": "category-1-total",
                            "desc": "Category 1 Total desc."
                        },
                        "categories": [
                            {
                                "code": "category_1_1_code",
                                "name": "Category 1_1",
                                "slug": "category-1-1",
                                "desc": "Category 1_1 desc."
                            },
                            {
                                "code": "category_2_1_code",
                                "name": "Category 2_1",
                                "slug": "category-2-1",
                                "desc": "Category 2_1 desc.",
                                "sub-categories": [
                                    {
                                        "code": "sub-category_2_1_1_code",
                                        "name": "Sub-category 2_1_1",
                                        "slug": "sub-category-2-1-1",
                                        "desc": "Sub-category 2_1_1 desc."
                                    },
                                    {
                                        "code": "sub-category_2_1_2_code",
                                        "name": "Sub-category 2_1_2",
                                        "slug": "sub-category-2-1-2",
                                        "desc": "Sub-category 2_1_2 desc."
                                    },
                                    {
                                        "code": "sub-category_2_1_3_code",
                                        "name": "Sub-category 2_1_3",
                                        "slug": "sub-category-2-1-3",
                                        "desc": "Sub-category 2_1_3 desc."
                                    },
                                ]
                            },
                            {
                                "code": "category_3_1_code",
                                "name": "Category 3_1",
                                "slug": "category-3-1",
                                "desc": "Category 3_1 desc."
                            },
                        ]
                    },
                    {
                        "code": "classification_2_code",
                        "name": "Classification 2",
                        "slug": "classification-2",
                        "desc": "Classification 2 desc.",
                        "units": "units_2",
                        "total": {
                            "code": "category_2_0001",
                            "name": "Category 2 Total",
                            "slug": "category-2-total",
                            "desc": "Category 2 Total desc."
                        },
                        "categories": [
                            {
                                "code": "category_2_1_code",
                                "name": "Category 2_1",
                                "slug": "category-2-1",
                                "desc": "Category 2_1 desc."
                            },
                            {
                                "code": "category_2_2_code",
                                "name": "Category 2_2",
                                "slug": "category-2-2",
                                "desc": "Category 2_2 desc."
                            },
                            {
                                "code": "category_2_3_code",
                                "name": "Category 2_3",
                                "slug": "category-2-3",
                                "desc": "Category 2_3 desc."
                            },
                        ]
                    },
                ]
            }
        ]
        returned = self.read_test_JSON()
        self.assertEqual(expected, returned)

    def test_content_csv_to_json_blank_cat_desc_placeholder(self):
        # GIVEN we have written a csv with one topic and one table with one categories and one subcategory, all
        # with blank descriptions
        self.write_test_CSV([
            ["name","desc","taxonomy","code","units"],
            ["Topic 1", "", "topic", "", ""],
            ["Classification 1", "", "classification", "classification_1_code", "units_1"],
            ["Category 1 Total", "", "category", "category_1_0001", ""],
            ["Category 1_1", "", "category", "category_1_1_code", ""],
            ["Sub-category 1_1_1", "","sub-category", "sub-category_1_1_1_code", ""],
        ])
        
        # WHEN we run the csv_to_meta script
        os.system(f"python csv_to_meta.py {self.test_fp}")

        # THEN we expect to get a properly formatted JSON back, with lorem ipsum placeholder descriptions
        expected = [
            {
                "code": "Topic 1",
                "name": "Topic 1",
                "slug": "topic-1",
                "desc": DESC_PLACEHOLDER,
                "classifications": [
                    {
                        "code": "classification_1_code",
                        "name": "Classification 1",
                        "slug": "classification-1",
                        "desc": DESC_PLACEHOLDER,
                        "units": "units_1",
                        "total": {
                            "code": "category_1_0001",
                            "name": "Category 1 Total",
                            "slug": "category-1-total",
                            "desc": DESC_PLACEHOLDER
                        },
                        "categories": [
                            {
                                "code": "category_1_1_code",
                                "name": "Category 1_1",
                                "slug": "category-1-1",
                                "desc": DESC_PLACEHOLDER,
                                "sub-categories": [
                                    {
                                        "code": "sub-category_1_1_1_code",
                                        "name": "Sub-category 1_1_1",
                                        "slug": "sub-category-1-1-1",
                                        "desc": DESC_PLACEHOLDER
                                    },
                                ]
                            },
                        ]
                    }
                ]
            }
        ]
        returned = self.read_test_JSON()
        self.assertEqual(expected, returned)
