import json
import pathlib
import re
import sys

from csv import DictReader

def slugify(name):
    return "-".join(re.sub(r"[^a-zA-Z0-9]", " ", name.lower()).split())

def main(fp):

    # load csv
    with open(fp) as f:
        rows = DictReader(f)
        curr_topic = {}
        curr_table = {}
        topics = []
        for row in rows:
            
            # if topic class write out old topic unless its empty and reset
            if row['class'] == 'topic':
                if curr_topic:
                    if curr_table:
                        curr_topic['tables'].append(curr_table)
                        curr_table = {}
                    topics.append(curr_topic)
                curr_topic = {
                    "code": row['name'],
                    "name": row['name'],
                    "slug": slugify(row['name']),
                    "desc": row['desc'],
                    "tables": []
                }
                
            
            # if table class write out old table unless its empty and reset, NB ignore tables with no code
            if row['class'] == 'table' and row['nomis_code'] != "":
                print(row)
                if curr_table:
                    curr_topic['tables'].append(curr_table)
                curr_table = {
                    "code": row['nomis_code'],
                    "name": row['name'],
                    "slug": slugify(row['name']),
                    "desc": row['desc'],
                    "categories": []
                }

            if row['class'] in ('category', 'sub-category') and row['nomis_code'] != "":

                # units are in the categories and need some translation
                if row['nomis_units'] == 'Person':
                    curr_table['units'] = "People"
                else:
                    curr_table['units'] = "Households"
                category = {
                    "code": row['nomis_code'],
                    "name": row['name'],
                    "slug": slugify(row['name'])
                }
                if row['nomis_code'].endswith('0001'):
                    curr_table['total'] = category
                else:
                    curr_table['categories'].append(category)

        # if we still have a topic after the loop, write it
        if curr_topic:
            if curr_table:
                curr_topic['tables'].append(curr_table)
            topics.append(curr_topic) 


    with open(fp.with_suffix(".apiMetadata.json"), 'w') as f:
       json.dump(topics, f, indent=2)


if __name__=="__main__":
    fp = pathlib.PurePath(sys.argv[1])
    main(fp)