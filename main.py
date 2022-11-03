import pandas as pd
import re
import json
import numpy as np
import os
import requests
from collections import OrderedDict


def ordered(d, desired_key_order):
    return OrderedDict([(key, d[key]) for key in desired_key_order])


desired_key_order = ("@context", "@id", "@type", "label", "metadata", "structures", "sequences")


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

    group_key = csv.loc[groups[key]]
    group_mag = group_key.groupby(['Reference3']).indices
    start_json_url = dlcs_json

    json_req = requests.get(dlcs_json).json()
    json_req['structures'] = []
    for j, mag in enumerate(group_mag.keys()):
        index_page = group_mag[mag][0]
        # ref3 = csv.loc[group_mag[mag][0]]["Reference3"]
        ref3 = mag

        structure = {
            "@id": "https://dlc.services/iiif-resource/7/string1/72820760-01/range/{}".format(j),
            "@type": "sc:Range",
            "label": "Nr. {}".format(ref3.replace("%20", " ")),
            "canvases": [
                json_req["sequences"][0]["canvases"][index_page]["@id"]
            ],
            "within": ""
        }
        json_req['structures'].append(structure)
    json_req["metadata"] = [
        {"label": "Title",
         "value": "TU Delta"},
        {"label": "Author(s)",
         "value": ""},
        {"label": "Year",
         "value": ref2},
        {"label": "Yearnr.",
         "value": str(i + 15)}
    ]

    json_req["label"] = "Delta, Jaargang {} ({})".format(str(i + 15), ref2)
    json_req = ordered(json_req, desired_key_order)

    json_year = json.dumps(json_req, indent=8)

    with open(year_filename, "w") as outfile:
        outfile.write(json_year)

json_object = json.dumps(json_out, indent=5)
json_filename = "testtest"
with open("{}.json".format(json_filename), "w") as outfile:
    outfile.write(json_object)
