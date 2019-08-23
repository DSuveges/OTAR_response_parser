# OTAR parser

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ab0fc19c6def4bffb44ce6d89f75df85)](https://www.codacy.com/app/DSuveges/OTAR_response_parser?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=DSuveges/OTAR_response_parser&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/DSuveges/OTAR_response_parser.svg?branch=master)](https://travis-ci.org/DSuveges/OTAR_response_parser)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/ab0fc19c6def4bffb44ce6d89f75df85)](https://www.codacy.com/app/DSuveges/OTAR_response_parser?utm_source=github.com&utm_medium=referral&utm_content=DSuveges/OTAR_response_parser&utm_campaign=Badge_Coverage)

This module is an extension of the [Python client for the Open Targets REST API](https://github.com/opentargets/opentargets-py) 
that parses the result object. The module has a simple command line interfact to demonstrate its functionality by displaying 
summaries of the overlall association scores in a returned response object.

#### Requirements

* Python 3.6+
* Opentargets 3.1.16 (see installation instruction [here](https://opentargets.readthedocs.io/en/stable/))

## Installation using pip

1. Clone repository from github:
    ```bash
    git clone https://github.com/DSuveges/OTAR_response_parser.git
    cd OTAR_response_parser
    ```

2. Setting up environment:
    
    ```bash
    python3 -m venv OTP
    source OTP/bin/activate
    ```
3. Installing parser module and all its dependencies:

    ```bash
    pip install .
    ```

## Installation using docker

To be added later

## Usage

### The command line interface

**Display command line help message:**

```bash
OTAR_result_parser -h
``` 

Expected output:
```
usage: OTAR_result_parser [-h] [-t TARGET] [-d DISEASE] [-v]

A small tool to retrieve association information from Opentargets based on a
provided target or disease.

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Target name eg. ENSG00000197386.
  -d DISEASE, --disease DISEASE
                        Name of schema eg. association. eg. Orphanet_399
  -v, --verbose         Prints out extra information
```

**Parsing result object for a target query:**

```bash
OTAR_result_parser -t ENSG00000197386
``` 

Expected output:

```
[Info] The maximum of the association_score.overall values: 1.0
[Info] The minimum of the association_score.overall values: 0.004
[Info] The average of the association_score.overall values: 0.22693400415219542
[Info] The standard error of the association_score.overall values: 0.17547453440391447
```

**Parsing result object for a target query:**

```bash
OTAR_result_parser -d Orphanet_399
``` 

Expected output:

```
[Info] The maximum of the association_score.overall values: 1.0
[Info] The minimum of the association_score.overall values: 0.004
[Info] The average of the association_score.overall values: 0.0827557783951425
[Info] The standard error of the association_score.overall values: 0.15081103935000872
```

### Application interface

```python
from opentargets import OpenTargetsClient
from OTAR_result_parser.OTAR_result_parser import OTAR_result_parser

# Get association for a gene for example:
geneID = 'ENSG00000197386'

# Fetch data from OpenTargets:
client = OpenTargetsClient()
otar_results = client.filter_associations()
x = otar_results.filter(target=geneID)

# Initialize parser object:
OT_parser = OTAR_result_parser(x, verbose=True)
```

**Get the average of the overlall association scores:**

```python
OT_parser.get_association_score_mean()
```

**Get the lowest overlall association score:**

```python
OT_parser.get_association_score_min()
```
**Get the highest overlall association score:**

```python
OT_parser.get_association_score_max()
```
**Get the standard deviation of the overlall association scores:**

```python
OT_parser.get_association_score_std()
```

**Get the number of associations in the returned dataset:**

```python
len(OT_parser)
```