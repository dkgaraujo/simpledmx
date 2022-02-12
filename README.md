# simpledmx

`simpledmx` is a minimalistic Python package experience with SDMX that fetches all data from sources defined by the user. 

Although [SDMX](www.sdmx.org) is very flexible, the main use case of `simpledmx` is when a user wants to download all available data from a specific source(s), for a given frequency (eg, annual, semi-annual, quarterly, monthly, daily). `simpledmx` uses `pandasdmx` as the backend to explore and fetch datasets from sources using SDMX. Further details on the sources and dataflows can be found in the `pandasdmx` [documentation](https://pandasdmx.readthedocs.io/en/v1.0/).

## Install

`simpledmx` can be installed from pip:

```
$ pip install simpledmx
```

## Usage

Users are encouraged to first see the avaiable list of sources:

```
from simpledmx import list_sdmx_sources

list_sdmx_sources()
```
Once the desired sources have been identified, users can download a Pandas `DataFrame` with the following code:

```
from simpledmx import get_sdmx_data

df = get_sdmx_data(
    start_date='2016',
    end_date='2020',
    freq='A',
    sources=['BIS', 'ECB']
    )
```

Two things should be noted:
* The speed depends on the amount of data to be parsed and downloaded. Depending on the request, it can get slow.
* Some sources do not provide messages in a way that the backend library, `pandasdmx`, is able to parse. Hence, some sources may not work.

## Known issues

* `simpledmx` returns only the data, not the variable names. The user can learn more about the specific data at hand from the column names: each variable starts with its source, then the dataflow, followed by the key(s) (except for the time period) of that specific dataflow. 
* in some cases, parsing the files downloaded from the original sources can take a long time. This is an issue with XML parsing, not with `simpledmx` or its backend (`pandasdmx`) specifically.
