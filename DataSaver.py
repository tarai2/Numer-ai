import requests
import numpy as np
import pandas as pd


def get_main_universe():
    try:
        # download
        res = requests.get(
            "https://numerai-quant-public-data.s3-us-west-2.amazonaws.com/example_predictions/latest.csv"
        ).content
        df = pd.read_csv(io.StringIO(res.decode('utf-8')), header=0, index_col=0)

        # reform
        universe =\
            pd.DataFrame(
                [val.split(" ") for val in df.index.values],
                columns=["stock_id", "region"]
            ).fillna("blank", inplace=True)

        # extract & replace
        main_universe_region\
            = universe.groupby("region").count().sort_values(by="stock_id").tail(8).index.values
        main_universe = universe\
            .query("region in @main_universe_region")\
            .replace({
                "blank": "",
                "JT": ".T",
                "KS": ".KS",
                "LN": ".L",
                "AU": ".AX",
                "GY": ".DE",
                "FP": ".PA"
            })
        # USのidの末尾の.を消す
        main_universe.stock_id = main_universe.stock_id.apply(lambda x: x.replace(".", ""))

        # sumしてYahooFinanceIDに直す
        main_universe = main_universe.sum(axis=1).reset_index(drop=True)
        return main_universe

    except Exception as e:
        print(e)
