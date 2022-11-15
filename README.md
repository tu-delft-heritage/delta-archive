# Delta Archief

This repository contains [IIIF Presentation Manifests](https://iiif.io) of the following digitised magazines of Delft University of Technology:

- TH Mededelingen (1952-73)
- THD Nieuws (1968-82)
- Delta (1982-2017)
- Delft Integraal (1984-2021)
- Delft Outlook (1985-2021)
- Owee (special editions, 1998-9)

The complete collection can be opened in [Universal Viewer](https://universalviewer.io) by following this url:

- [https://tu-delft-library.github.io/delta-archief/](https://tu-delft-library.github.io/delta-archief/)

Alternatively, [Mirador](https://projectmirador.org) can be used:

- [https://projectmirador.org/embed/?manifest=https://tu-delft-library.github.io/delta-archief/manifests/delta-archief.json](https://projectmirador.org/embed/?manifest=https://tu-delft-library.github.io/delta-archief/manifests/delta-archief.json)

The magazines were scanned in 2021 by [GMS](https://gmsnl.com). The project was funded by Delta (Delta), Alumni Relations (Delft Integraal and Delft Outlook) and the Academic Heritage Team of TU Delft Library (THD Nieuws).

The images are hosted at the [DLCS](https://dlcs.info), part of the infrastructure for presenting the digital special collections TU Delft Library. The DLCS supports queries based on ingested strings, returning IIIF Presentation Manifests of collections of images. The following query for example returns Volume 1 (1952-53) of TH Mededelingen:

- [https://dlc.services/iiif-resource/7/string1string2string3/th-mededelingen/1952](https://dlc.services/iiif-resource/7/string1string2string3/th-mededelingen/1952)

This so-called skeleton manifest lack structures (table of contents) or metadata. This repository contains a Python script that adds the missing properties to the JSON manifests. The script also generates IIIF Collection Manifests for each magazine. It uses the information available in the `/csv` folder about the uploaded images.
