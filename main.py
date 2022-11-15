import pandas as pd
import re
import json
import numpy as np
import os
import requests
from collections import OrderedDict
import re
from pathlib import Path


def num_sort(test_string):
    if str(test_string).isdigit():
        out = test_string
    else:
        out = list(map(int, re.findall(r'\d+', test_string)))[0]
    return out


def ordered(d, desired_key_order):
    return OrderedDict([(key, d[key]) for key in desired_key_order])


desired_key_order = ("@context", "@id", "@type", "label", "metadata", "structures", "sequences")


class Meta:
    def __init__(self, title, author, year, worldcat):
        self.title = title
        self.author = author
        self.year = year
        self.worldcat = worldcat


csv = pd.read_csv('csv/Owee.csv')
Meta.title = "Oweekrant"
Meta.author = "Delft: Technische Hogeschool"
Meta.worldcat = 'N/A'

start_jaargang = 1

dlcs_base = "https://dlc.services/iiif-resource/7/string1string2string3/{}/{}"

groups = csv.groupby(['Reference1', 'Reference2']).indices
#
# Meta.year = "{}-{}".format(min(re.findall(r'\d{4}', csv['Reference2'].min())),
#                            max(re.findall(r'\d{4}', csv['Reference2'].max())))

Meta.year = "{}-{}".format(csv['Reference2'].min(),
                           str(csv['Reference2'].max())[2:])
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
            "@id": "https://tu-delft-library.github.io/delta-archief/manifests/{}/{}.json"
            .format(Meta.title.replace(" ", "-").lower(), Meta.title.replace(" ", "-").lower()),
            "@type": "sc:Collection",
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "manifests": []}

for i, key in enumerate(groups.keys()):
    ref1 = key[0]
    ref2 = key[1]

    if Meta.title == 'Delft Integraal':
        dlcs_json = dlcs_base.format(ref1.lstrip("nl-"), ref2)
    elif Meta.title == 'Delft Outlook':
        dlcs_json = dlcs_base.format(ref1.lstrip("en-"), ref2)
    else:
        dlcs_json = dlcs_base.format(ref1, ref2)

    if Meta.title == 'THD Nieuws':
        if str(ref2).isdigit():
            # jaar = str(ref2) + "-" + str(np.int_(ref2) + 1)[2:]
            # jaar = str(np.int_(ref2)-1)+"-"+str(ref2)[2:]
            if len(str(ref2)) > 4:
                jaar = str(ref2)[:4]+"-"+str(ref2)[-2:]
            else:
                jaar = str(np.int_(ref2) - 1) + "-" + str(ref2)[2:]
        else:
            jaar = ref2
    elif Meta.title == 'TH Mededelingen':
        if str(ref2).isdigit():
            # jaar = str(ref2) + "-" + str(np.int_(ref2) + 1)[2:]
            # jaar = str(np.int_(ref2)-1)+"-"+str(ref2)[2:]
            if len(str(ref2)) > 4:
                jaar = str(ref2)[:4]+"-"+str(ref2)[-2:]
            else:
                jaar = str(ref2)[2:] + "-" + str(np.int_(ref2) + 1)
        else:
            jaar = ref2
    else:
        jaar = ref2
    year_filename = "{}-{}.json".format(ref1.lower(), jaar)

    ref_id = "https://tu-delft-library.github.io/delta-archief/manifests/{}/{}"\
        .format(Meta.title.replace(" ", "-").lower(), year_filename)
    mani = {"@id": ref_id,
            "label": str(jaar),
            "@type": "sc:Manifest"}

    json_out["manifests"].append(mani)

    group_key = csv.loc[groups[key]]
    group_mag = group_key.groupby(['Reference3']).indices
    start_json_url = dlcs_json

    json_req = requests.get(dlcs_json).json()
    json_req['structures'] = []
    mag_key_list = list(group_mag.keys())

    mag_key_list.sort(key=num_sort)

    for j, mag in enumerate(mag_key_list):
        # if len(str(mag)) == 1:
        #     mag = str(mag).zfill(2)
        if any(item == Meta.title for item in ['Delft Outlook', 'Oweekrant']):
            index_page = group_mag[mag][0]
        else:
            index_page = group_mag[str(mag)][0]
        ref3 = mag
        if str(ref3).isalpha():
            struct_label = ref3
        else:
            struct_label = "Nr. {}".format(ref3)
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

    if int(str(ref2)[:4]) < 1986:
        Meta.author = "Delft: Technische Hogeschool"
    elif int(str(ref2)[:4]) == 1986:
        Meta.author = "Delft: Technische Hogeschool / Technische Universiteit"
    else:
        Meta.author = "Delft: Technische Universiteit"


    json_req["metadata"] = [
        {"label": "Titel",
         "value": Meta.title},
        {"label": "Uitgever",
         "value": Meta.author},
        {"label": "Jaargang",
         "value": str(i + start_jaargang)+" ("+str(jaar)+")"},
        {"label": "Worldcat",
         "value": Meta.worldcat}
    ]

    json_req["label"] = "{}, Jaargang {} ({})".format(Meta.title, str(i + start_jaargang), jaar)
    json_req = ordered(json_req, desired_key_order)

    json_year = json.dumps(json_req, indent=8)
    Path("manifests/"+Meta.title.replace(" ", "-").lower()).mkdir(parents=True, exist_ok=True)
    with open("manifests/"+Meta.title.replace(" ", "-").lower()+"/"+year_filename, "w") as outfile:
        outfile.write(json_year)

json_object = json.dumps(json_out, indent=5)
json_filename = Meta.title.replace(" ", "-").lower()
with open("manifests/"+Meta.title.replace(" ", "-").lower()+"/{}.json".format(json_filename), "w") as outfile:
    outfile.write(json_object)
