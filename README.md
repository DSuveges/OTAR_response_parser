# OTAR parser

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ab0fc19c6def4bffb44ce6d89f75df85)](https://www.codacy.com/app/DSuveges/OTAR_response_parser?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=DSuveges/OTAR_response_parser&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/DSuveges/OTAR_response_parser.svg?branch=master)](https://travis-ci.org/DSuveges/OTAR_response_parser)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/ab0fc19c6def4bffb44ce6d89f75df85)](https://www.codacy.com/app/DSuveges/OTAR_response_parser?utm_source=github.com&utm_medium=referral&utm_content=DSuveges/OTAR_response_parser&utm_campaign=Badge_Coverage)

This module is an extension of the [Python client for the Open Targets REST API](https://github.com/opentargets/opentargets-py) 
that parses the result object. The module has a simple command line interface to demonstrate its functionality by displaying 
summaries of the overall association scores extracted from the returned response object.

#### Requirements

* Python 3.6+
* Opentargets REST API wrapper v3.1.16 (see installation instruction [here](https://opentargets.readthedocs.io/en/stable/))

## Installation using pip

Once the desired Python virtual environment is activated, the parser and its dependencies can be directly installed from 
github using pip:

```bash
pip install git+https://github.com/DSuveges/OTAR_response_parser
```

## Usage

This is a Python module that takes `opentargets.conn.IterableResult` object as an input, but for demonstrative 
purposes, it is shipped with a simple command line interface as well. If the module is installed via `pip`, this 
command line tool gets also installed and added into the path. 

### The command line interface

**Display command line help message:**

```bash
OTAR_result_parser -h
``` 

Expected output:
```
usage: OTAR_result_parser [-h] [-t TARGET] [-d DISEASE] [-v]

A small command line tool to demonstrate the capabilities of the Opentargets
parser module. At this stage it shows statistics of the association scores in
a result set of a target or disease specific query.

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Specify target ID. eg. ENSG00000197386.
  -d DISEASE, --disease DISEASE
                        Specify disease ID. eg. Orphanet_399
  -v, --verbose         Prints out extra information
```

**Parsing result object for a target query:**

```bash
OTAR_result_parser -t ENSG00000197386
``` 

Expected output:

```
Assoc #0 - Target ID: ENSG00000197386, disease ID: EFO_0000618, association score: 1.0
Assoc #1 - Target ID: ENSG00000197386, disease ID: Orphanet_71859, association score: 1.0
...
Assoc #791 - Target ID: ENSG00000197386, disease ID: EFO_0003758, association score: 0.004
Assoc #792 - Target ID: ENSG00000197386, disease ID: EFO_0003756, association score: 0.004

[Info] The maximum of the association_score.overall values: 1.0
[Info] The minimum of the association_score.overall values: 0.004
[Info] The average of the association_score.overall values: 0.22693400415219542
[Info] The standard error of the association_score.overall values: 0.17547453440391447
```

**Parsing result object for a disease query:**

```bash
OTAR_result_parser -d Orphanet_399
``` 

Expected output:

```
Assoc #0 - Target ID: ENSG00000165646, disease ID: Orphanet_399, association score: 1.0
Assoc #1 - Target ID: ENSG00000198785, disease ID: Orphanet_399, association score: 1.0
...
Assoc #798 - Target ID: ENSG00000101966, disease ID: Orphanet_399, association score: 0.004
Assoc #799 - Target ID: ENSG00000006128, disease ID: Orphanet_399, association score: 0.004

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

**Get the average of the overall association scores:**

```python
OT_parser.get_association_score_mean()
```

**Get the lowest overall association score:**

```python
OT_parser.get_association_score_min()
```
**Get the highest overall association score:**

```python
OT_parser.get_association_score_max()
```
**Get the standard deviation of the overall association scores:**

```python
OT_parser.get_association_score_std()
```

**Get the number of associations in the returned dataset:**

```python
len(OT_parser)
```