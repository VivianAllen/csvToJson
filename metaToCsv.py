import csv
import json


def load_meta():
    with open("./meta.json") as f:
        meta_json = json.load(f)
    return meta_json


def topicsCSV(meta_json):
    with open('original_topics.csv', 'w') as f:
        fieldnames = ["Code / Short Name", "Display Name", "Descriptive Text"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for topic in meta_json:
            writer.writerow(
                {
                    "Code / Short Name": topic["code"],
                    "Display Name": topic["name"],
                    "Descriptive Text": ""
                }
            )

def tableCSV(meta_json):
    with open('original_tables.csv', 'w') as f:
        fieldnames = ["Code / Short Name", "Display Name", "Descriptive Text", "Topic"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for topic in meta_json:
            if topic["tables"] is not None:
                for table in topic["tables"]:
                    writer.writerow(
                        {
                            "Code / Short Name": table["code"],
                            "Display Name": table["name"],
                            "Descriptive Text": "",
                            "Topic": topic["code"]
                        }
                    )


def categoryCSV(meta_json):
    with open('original_categories.csv', 'w') as f:
        fieldnames = ["Code / Short Name", "Display Name", "Descriptive Text", "Table"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for topic in meta_json:
            if topic["tables"] is not None:
                for table in topic["tables"]:
                    if table["categories"] is not None:
                        for category in table["categories"]:
                            writer.writerow(
                                {
                                    "Code / Short Name": category["code"],
                                    "Display Name": category["name"],
                                    "Descriptive Text": "",
                                    "Table": table["code"],
                                }
                            )

if __name__=="__main__":
    meta_json = load_meta()
    topicsCSV(meta_json)
    tableCSV(meta_json)
    categoryCSV(meta_json)