import json
import re

from csv import DictWriter

if __name__=="__main__":
    # load raw csv
    with open("./Find Insights Alpha - Census Atlas Information Architecture V3.csv") as f:
        miro_lines = f.readlines()

    # iterate through and pull out relevant lines as objects
    target_re = re.compile(r"\"(.*)#([\d-]+)#")
    desc_split_re = re.compile(r"-{4,}")
    census_metadata = {"children": {}}
    for line in miro_lines:
        # skip lines without something matching digits and dashes between two hashtags
        match = target_re.match(line)
        if match:
            # parse line   
            groups = match.groups()
            
            # ensure census_metadata has a home for the parsed_line
            parsed_line_home = census_metadata
            nestings = groups[1].split('-')
            for nesting in nestings:
                # might as well do sorting while we're here...
                parsed_line_home["children"] = {k: parsed_line_home["children"][k] for k in sorted(parsed_line_home["children"])}
                parsed_line_home = parsed_line_home["children"].setdefault(int(nesting), {"children": {}})

            # if descriptive text has more than four consecutive dashes it splits into name and desc
            desc_text = groups[0]
            desc_match = desc_split_re.search(desc_text)
            parsed_line_home["id"] = groups[1]
            parsed_line_home["parent"] = '-'.join(nestings[:-1])
            if desc_match:
                name, desc = desc_split_re.split(desc_text)
                parsed_line_home["name"] = name.strip()
                parsed_line_home["desc"] = desc.strip()
            else:
                parsed_line_home["name"] = desc_text.strip()
                parsed_line_home["desc"] = None
            
            if len(nestings) == 1:
                parsed_line_home["class"] = "topic"
            elif len(nestings) == 2:
                parsed_line_home["class"] = "table"
            elif len(nestings) == 3:
                parsed_line_home["class"] = "category"
            else:
                parsed_line_home["class"] = "sub-category"

            parsed_line_home["nomis_code"] = ""
            parsed_line_home["notes"] = ""
    
    # print to csv
    def nested_appender(census_metadata_object):
        if "id" in census_metadata_object:
            csv_lines.append(
                {
                    "id": census_metadata_object["id"],
                    "parent": census_metadata_object["parent"],
                    "name": census_metadata_object["name"],
                    "desc": census_metadata_object["desc"],
                    "class": census_metadata_object["class"],
                    "nomis_code": census_metadata_object["nomis_code"],
                    "notes": census_metadata_object["notes"]
                }
            )
        for _, child in census_metadata_object["children"].items():
            nested_appender(child)
        return
    csv_lines = []
    nested_appender(census_metadata)
    with open('Find Insights Alpha - Census Atlas Information Architecture V3 parsed.csv', 'w') as f:
        writer = DictWriter(f, fieldnames=csv_lines[0].keys())
        writer.writeheader()
        writer.writerows(csv_lines)
