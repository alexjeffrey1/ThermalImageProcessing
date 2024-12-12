# Read out IS2 files
This script is written to read out the IS2 files made by a Fluke Ti480 Pro.

The conversion between the IR-data and temperature is defined by the IS2-file itself. The accuracy in relation to the Fluke software is now <5 K.


## Setup
Create a virtual environment (only first time):

`python3 -m virtualenv -p python3 .`

Activate the virtual environment:

`source bin/activate` or `. bin/activate`

Install requirements (only first time):

`pip install -r requirements.txt`

## Usage
Standalone script which generates plots:

`python readis2.py [-h] [-m COLORMAP] [-l LIMITS] [-c CONTOURPLOT] [-e EMISSIVITY] [-t TRANSMISSION] [-b BACKGROUNDTEMP] [-s TEMPSCALE] [-S SAVEAS] [-g GRID] [--label LABEL] [-a ANGLE] [-T TITLE] filename`

To use it in your own project:

```
import readis2.read_is2_new as readis2

data = readis2(filename)
```
