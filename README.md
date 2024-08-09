# Delta Archive

This repository contains [IIIF Presentation Manifests](https://iiif.io) of the following digitised magazines of Delft University of Technology:

- TH Mededelingen (1952-73)
- THD Nieuws (1968-82)
- Delta (1982-2017)
- Delft Integraal (1984-2021)
- Delft Outlook (1985-2021)
- Owee (special editions, 1998-9)

The complete collection can be opened in [Universal Viewer](https://universalviewer.io) by following this url:

- [https://tu-delft-heritage.github.io/delta-archive/](https://tu-delft-heritage.github.io/delta-archive/)

Alternatively, [Mirador](https://projectmirador.org) can be used:

- [https://projectmirador.org/embed/?manifest=https://tu-delft-heritage.github.io/delta-archive/manifests/delta-archive.json](https://projectmirador.org/embed/?manifest=https://tu-delft-heritage.github.io/delta-archive/manifests/delta-archive.json)

Links to the invidual magazines:

| Magazine | IIIF Manifest | Universal Viewer | Mirador | Total number of pages |
| ---  | --- | --- | --- | --- |
TH Mededelingen | [Open](https://tu-delft-heritage.github.io/delta-archive/manifests/th-mededelingen/th-mededelingen.json) | [Open](http://universalviewer.io/uv.html?manifest=https://tu-delft-heritage.github.io/delta-archive/manifests/th-mededelingen/th-mededelingen.json) | [Open](https://projectmirador.org/embed/?manifest=https://tu-delft-heritage.github.io/delta-archive/manifests/th-mededelingen/th-mededelingen.json) | 3.248
THD Nieuws | [Open](https://tu-delft-heritage.github.io/delta-archive/manifests/thd-nieuws/thd-nieuws.json) | [Open](http://universalviewer.io/uv.html?manifest=https://tu-delft-heritage.github.io/delta-archive/manifests/thd-nieuws/thd-nieuws.json) | [Open](https://projectmirador.org/embed/?manifest=https://tu-delft-heritage.github.io/delta-archive/manifests/thd-nieuws/thd-nieuws.json) | 6.166 |
Delta | [Open](https://tu-delft-heritage.github.io/delta-archive/manifests/delta/delta.json) | [Open](http://universalviewer.io/uv.html?manifest=https://tu-delft-heritage.github.io/delta-archive/manifests/delta/delta.json) | [Open](https://projectmirador.org/embed/?manifest=https://tu-delft-heritage.github.io/delta-archive/manifests/delta/delta.json) | 25.239 |
Delft Integraal | [Open](https://tu-delft-heritage.github.io/delta-archive/manifests/delft-integraal/delft-integraal.json) | [Open](http://universalviewer.io/uv.html?manifest=https://tu-delft-heritage.github.io/delta-archive/manifests/delft-integraal/delft-integraal.json) | [Open](https://projectmirador.org/embed/?manifest=https://tu-delft-heritage.github.io/delta-archive/manifests/delft-integraal/delft-integraal.json) | 5679 |
Delft Outlook | [Open](https://tu-delft-heritage.github.io/delta-archive/manifests/delft-outlook/delft-outlook.json) | [Open](http://universalviewer.io/uv.html?manifest=https://tu-delft-heritage.github.io/delta-archive/manifests/delft-outlook/delft-outlook.json) | [Open](https://projectmirador.org/embed/?manifest=https://tu-delft-heritage.github.io/delta-archive/manifests/delft-outlook/delft-outlook.json) | 4066 |
Owee | [Open](https://tu-delft-heritage.github.io/delta-archive/manifests/owee/owee.json) | [Open](http://universalviewer.io/uv.html?manifest=https://tu-delft-heritage.github.io/delta-archive/manifests/owee/owee.json) | [Open](https://projectmirador.org/embed/?manifest=https://tu-delft-heritage.github.io/delta-archive/manifests/owee/owee.json) | 90 |
| Totaal | [Open](https://tu-delft-heritage.github.io/delta-archive/manifests/delta-archive.json) | [Open](https://tu-delft-heritage.github.io/delta-archive/) | [Open](https://projectmirador.org/embed/?manifest=https://tu-delft-heritage.github.io/delta-archive/manifests/delta-archive.json) | 44.438 | 

## Background

The magazines were digitised in 2021 by [GMS](https://gmsnl.com). The project was funded by Delta (Delta), Alumni Relations (Delft Integraal and Delft Outlook) and the Academic Heritage Team of TU Delft Library (THD Nieuws). Please note that some of the volumes might not be complete due to missing issues in the archive of Delta or the collection of TU Delft Library.

The images are hosted at the [DLCS](https://dlcs.info), part of the infrastructure for presenting the digital special collections of TU Delft Library. The DLCS supports queries based on ingested strings, returning IIIF Presentation Manifests of matching images. The following query for example returns Volume 1 (1952-53) of TH Mededelingen:

- [https://dlc.services/iiif-resource/7/string1string2string3/th-mededelingen/1952](https://dlc.services/iiif-resource/7/string1string2string3/th-mededelingen/1952)

These so-called skeleton manifests lack structures (table of contents) and metadata. This repository contains a Python script that adds the missing properties to JSON manifests of each volume. The script also generates IIIF Collection Manifests for each magazine. It uses the information available in the `/csv` folder about the uploaded images and strings. The resulting JSON manifests can be found in the `/manifests` folder. The following IIIF Collection Manifest lists all the available journals and is preloaded in the viewers linked above:

- [https://tu-delft-heritage.github.io/delta-archive/manifests/delta-archive.json](https://tu-delft-heritage.github.io/delta-archive/manifests/delta-archive.json)

## Todo

- Adding the magazines to the [academic heritage website](https://heritage.tudelft.nl/en). For this it needs to be possible to navigate structures of manifests.
- Adding full text search. This is part of a large puzzle to extend the capabilities of the digital infrastructure.
- Offering PDF downloads of individual issues or custom selected ranges. Same as above.
