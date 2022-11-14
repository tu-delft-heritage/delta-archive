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
    def __init__(self, title, author, year, worldcat):
        self.title = title
        self.author = author
        self.year = year
        self.worldcat = worldcat


csv = pd.read_csv('csv/th-mededelingen.csv')
Meta.title = "TH Mededelingen"
Meta.author = "Delft: Technische Hogeschool"
Meta.worldcat = '<a href="https://tudelft.on.worldcat.org/oclc/72820760">72820760</a>'

start_jaargang = 1

dlcs_base = "https://dlc.services/iiif-resource/7/string1string2string3/{}/{}"

groups = csv.groupby(['Reference1', 'Reference2']).indices
#
# Meta.year = "{}-{}".format(min(re.findall(r'\d{4}', csv['Reference2'].min())),
#                            max(re.findall(r'\d{4}', csv['Reference2'].max())))

Meta.year = "{}-{}".format(csv['Reference2'].min(),
                           csv['Reference2'].max())
meta = [{
    "label": "Titel",
    "value": Meta.title
    },
    # {
    #     "label": "Uitgave",
    #     "value": Meta.author
    # },
    {
        "label": "Year",
        "value": Meta.year
    },
    {
        "label": "Worldcat",
        "value": Meta.worldcat
    }]

json_out = {"label": Meta.title.replace("_", " "),
            "metadata": meta,
            "@id": "https://tu-delft-library.github.io/delta-archief/manifests/{}.json"
            .format(Meta.title.replace(" ", "-").lower()),
            "@type": "sc:Collection",
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "manifests": []}

for i, key in enumerate(groups.keys()):
    ref1 = key[0]
    ref2 = key[1]

    dlcs_json = dlcs_base.format(ref1.lstrip("en-"), ref2)
    if ref2.isdigit():
        jaar = str(ref2) + "-" + str(np.int_(ref2) + 1)[2:]
    else:
        jaar = ref2
    year_filename = "{}-{}.json".format(ref1.lower(), jaar)

    ref_id = "https://tu-delft-library.github.io/delta-archief/manifests/{}/{}"\
        .format(Meta.title.replace(" ", "-").lower(), year_filename)
    mani = {"@id": ref_id,
            "label": jaar,
            "@type": "sc:Manifest"}

    json_out["manifests"].append(mani)

    group_key = csv.loc[groups[key]]
    group_mag = group_key.groupby(['Reference3']).indices
    start_json_url = dlcs_json

    json_req = requests.get(dlcs_json).json()
    json_req['structures'] = []
    mag_key_list = list(group_mag.keys())
    for k, mag_key in enumerate(mag_key_list):
        if mag_key.isdigit():
            mag_key_list[k] = np.int_(mag_key)
        else:
            mag_key_list[k] = mag_key

    mag_keys = np.sort(mag_key_list)
    for j, mag in enumerate(mag_keys):
        index_page = group_mag[str(mag)][0]
        ref3 = mag
        if str(ref3).isdigit():
            struct_label = "Nr. {}".format(ref3)
        else:
            struct_label = ref3
        # ref3 = csv.loc[group_mag[mag][0]]["Reference3"]
        structure = {
            "@id": "https://dlc.services/iiif-resource/7/string1/72820760-01/range/{}".format(j),
            "@type": "sc:Range",
            "label": struct_label,
            "canvases": [
                json_req["sequences"][0]["canvases"][index_page]["@id"]
            ],
            "within": ""
        }
        json_req['structures'].append(structure)

    # if int(ref2) < 1986:
    #     uitgever = "Delft: Technische Hogeschool"
    # elif int(ref2) == 1986:
    #     uitgever = "Delft: Technische Hogeschool / Technische Universiteit"
    # else:
    #     uitgever = "Delft: Technische Universiteit"


    json_req["metadata"] = [
        {"label": "Titel",
         "value": Meta.title},
        {"label": "Uitgever",
         "value": Meta.author},
        {"label": "Jaargang",
         "value": str(i + start_jaargang)+" ("+jaar+")"},
        {"label": "Worldcat",
         "value": Meta.worldcat}
    ]

    json_req["label"] = "{}, Jaargang {} ({})".format(Meta.title, str(i + start_jaargang), jaar)
    json_req = ordered(json_req, desired_key_order)

    json_year = json.dumps(json_req, indent=8)

    with open("manifests/"+Meta.title.replace(" ", "-").lower()+"/"+year_filename, "w") as outfile:
        outfile.write(json_year)

json_object = json.dumps(json_out, indent=5)
json_filename = Meta.title.replace(" ", "-").lower()
with open("manifests/"+Meta.title.replace(" ", "-").lower()+"/{}.json".format(json_filename), "w") as outfile:
    outfile.write(json_object)
