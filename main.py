import pandas as pd
import re
import json
import numpy as np
import os
import requests


class Meta:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year


Meta.title = "TU Delta"
Meta.author = ""

dlcs_base = "https://dlc.services/iiif-resource/7/string1string2string3/{}/{}"

csv = pd.read_csv('tu-delta.csv')

groups = csv.groupby(['Reference1', 'Reference2']).indices



Meta.year = "{}-{}".format(min(re.findall(r'\d{4}', csv['Reference2'].min())),
                           max(re.findall(r'\d{4}', csv['Reference2'].max())))
meta = [{
            "label": "Title",
            "value": Meta.title
        },
        {
            "label": "Author(s)",
            "value": Meta.author
        },
        {
            "label": "Year",
            "value": Meta.year
        },
        {
            "label": "OCLC Number",
            "value": ""
        }]

json_out = {"label": Meta.title,
            "metadata": meta,
            "@id": "https://raw.githubusercontent.com/sammeltassen/iiif-manifests/master/journals/th-mededelingen.json",
            "@type": "sc:Collection",
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "manifests": []}

for i, key in enumerate(groups.keys()):
    ref1 = key[0]
    ref2 = key[1]

    dlcs_json = dlcs_base.format(ref1, ref2)
    year_filename = "{}_{}.json".format(ref1, ref2)
    ref_id = "https://raw.githubusercontent.com/tu-delft-library/Create_JSON_Manifests/main/{}".format(year_filename)
    mani = {"@id": ref_id,
            "label": ref2,
            "@type": "sc:Manifest"}

    json_out["manifests"].append(mani)

    group_mag = csv.loc[groups[key]].groupby(['Reference3']).indices
    start_json_url = dlcs_json

    json_req = requests.get(dlcs_json).json()
    json_req['structures'] = []
    for j, mag in enumerate(group_mag.keys()):
        index_page = group_mag[mag][0]
        ref3 = csv.loc[group_mag[mag][0]]["Reference3"]

        structure = {
          "@id": "https://dlc.services/iiif-resource/7/string1/72820760-01/range/{}".format(j),
          "@type": "sc:Range",
          "label": "Nr. {}".format(j+1),
          "canvases": [
            "https://dlc.services/iiif-query/7/?canvas=n2&manifest=s1&sequence=n1&s1=delta&n1=&n2={}".format(index_page)
          ],
          "within": ""
        }
        json_req['structures'].append(structure)

    json_year = json.dumps(json_req, indent=8)

    with open(year_filename, "w") as outfile:
        outfile.write(json_year)


json_object = json.dumps(json_out, indent=5)
json_filename = "testtest"
with open("{}.json".format(json_filename), "w") as outfile:
    outfile.write(json_object)


