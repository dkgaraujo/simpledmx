#    Copyright 2022 Douglas Kiarelly Godoy de Araujo

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

__version__ = "0.0.3"

import pandas as pd
import pandasdmx as sdmx

from tqdm import tqdm


def list_sdmx_sources():
    # Only sources that seem to work in a variety of cases are included below
    return sdmx.list_sources()


def get_sdmx_data(start_date, end_date, freq, sources=None, **kwargs):
    params = {"startPeriod": start_date, "endPeriod": end_date}
    key = {"FREQ": freq}

    if not sources:
        sources = list_sdmx_sources()

    smsgs, sessions = get_series_msgs(sources=sources, **kwargs)
    effective_sources = list(smsgs.keys())
    dflows = {src: list(smsgs[src].keys()) for src in effective_sources}
    dmsgs = get_data(smsgs, sessions, key=key, params=params, dflows=dflows)
    augm_data = aggregate_augm_data(dmsgs)
    try:
        df_augm = pd.concat(
            [pd.concat(augm_data[src], axis=1) for src, _ in augm_data.items()]
        )
        return df_augm
    except:
        return None


def get_sessions(sources: list, **kwargs):
    return {src: sdmx.Request(src, **kwargs) for src in sources}


def get_dataflows(sessions: dict):
    src_dflows = {}
    for src, session in sessions.items():
        try:
            dflows = session.dataflow()
        except:
            continue
        src_dflows[src] = dflows
    return src_dflows


def get_series_msgs(sources=None, **kwargs):
    if sources is None or (isinstance(sources, str) and sources.lower() == "all"):
        sources = list_sdmx_sources()
    if not isinstance(sources, list):
        sources = [sources]
    sessions = get_sessions(sources=sources, **kwargs)
    src_dflows = get_dataflows(sessions=sessions)
    dflows_names = {
        key: list(value.dataflow.keys()) for key, value in src_dflows.items()
    }

    series_msgs = {}
    for key, dflows in dflows_names.items():
        series_msgs[key] = {}
        for dflow in tqdm(dflows):
            msg = f"Source: {key}, dataflow: {dflow}"
            try:
                series_msgs[key][dflow] = sessions[key].dataflow(dflow)
                print(msg + " ok!")
            except:
                print(msg + " not available.")
                continue
    return series_msgs, sessions


def get_data(smsgs, sessions, key, params, dflows):
    sources = list(smsgs.keys())
    data_msg = {}
    for src in sources:
        if not dflows:
            dflows = list(smsgs[src].keys())
        data_msg[src] = {}
        for dflow in tqdm(dflows[src]):
            msg = f"Trying to download {dflow} from {src}..."
            try:
                data_msg[src][dflow] = sessions[src].data(dflow, key=key, params=params)
            except:
                print(msg + " not possible.")
                continue
            print(msg + " ok!")
    return data_msg


def aggregate_augm_data(data_msg):
    sources_used = list(data_msg.keys())
    augm_data = {}
    for src in sources_used:
        augm_data[src] = []
        dflows_used = list(data_msg[src].keys())
        for dflow in tqdm(dflows_used):
            print(f"Getting data from {src}'s {dflow}")
            data = data_msg[src][dflow].data[0]
            try:
                data = sdmx.to_pandas(data).to_frame()
                data = data.pivot_table(
                    values="value",
                    index="TIME_PERIOD",
                    columns=[col for col in data.index.names if col != "TIME_PERIOD"],
                )
                data.columns = data.columns.map("_".join).str.strip("_")
                data = data.add_prefix(src + "_" + dflow + "_")
                augm_data[src].append(data)
                print("Successful")
            except:
                continue
    return augm_data
