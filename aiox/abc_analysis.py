import numpy as np
import pandas as pd


def abc_analysis(
    df,
    primary_dimension,
    numeric_dimension,
    secondary_dimensions=None,
    A=0.8,
    B=0.95,
    classified_only=False,
):
    """
    Multi-Dimensional ABC Analysis provides ABC classification for a multi-dimensional, granular input.

    Parameters
    ----------
    df : Pandas.DataFrame
        DataFrame holding the object to be classified, if applicable additional secondary_dimensions, and
        numeric values used for classification, e.g.

        df.columns = ["product", "country", "quantity"].

    primary_dimension : string
        Column name in input DataFrame holding object to be classified, e.g. product.

    secondary_dimension : list of strings = None
        List of columns names in input DataFrame holding additional attributes of primary_dimension to
        structure classification on a more granular level, e.g. country, region, city

    numeric_dimension : string
        Column name in input DataFrame holding numeric values to be used for classification.

    A, B : float = 0.8, 0.95
        Threshold for classification.

    classified_only : bool = False
        Provides DataFrame with columns primary_dimension, secondary_dimension, numeric_dimension and class
        in originally provided naming.

    Returns
    -------
    df_grouped : Pandas.DataFrame
        input DataFrame grouped by provided primary- & secondary dimensions with respective
        classification and cumulative values.

    Examples
    --------
    >>> import aiox
    >>> # create sample data
    >>> products, quantities = {}, {}
    >>> np.random.seed(seed=0)
    >>> for i in range(1000):
    >>>     products[i] = "{:04d}".format(np.random.randint(15))
    >>>     quantities[i] = np.random.randint(1000)
    >>> # prepare sample data DataFrame
    >>> df = pd.DataFrame()
    >>> df["Product"] = products.values()
    >>> df["Quantity"] = quantities.values()
    >>>
    >>> results = aiox.abc_analysis(
    >>>     df, primary_dimension="Product", numeric_dimension="Quantity"
    >>> )
    """
    # assign input variables
    A, B = A, B

    columns = {
        primary_dimension: "primary_dimension",
        numeric_dimension: "numeric_dimension",
    }
    df = df.rename(columns=columns)

    if secondary_dimensions is None:
        df["secondary_dimension"] = "No secondary dimension provided"
    #         secondary_dimensions=["X"]
    #         return multi_dim_abc_analysis(df=df,master_dimension=master_dimension,secondary_dimensions="X",numeric_dimension=numeric_dimension)
    else:
        # aggregate secondary dimensions into one key column
        df["secondary_dimension"] = df[secondary_dimensions].agg("-".join, axis=1)

    # calculate cumsum for secondary dimension
    df_subsum = (
        df.groupby("secondary_dimension")
        .sum()
        .sort_values(by=(["secondary_dimension", "numeric_dimension"]), ascending=False)
        .reset_index()
    )

    # create return DataFrame in target grouping
    df_grouped = (
        df.groupby(["secondary_dimension", "primary_dimension"])
        .sum()
        .sort_values(by=(["secondary_dimension", "numeric_dimension"]), ascending=False)
        .reset_index()
    )

    # prepare DataFrame to calculate relative quantity
    dict_subsum = {k: list(v.values()) for k, v in df_subsum.to_dict("index").items()}
    for i in range(len(df_grouped["secondary_dimension"].unique())):
        df_grouped.loc[
            df_grouped["secondary_dimension"] == dict_subsum.get(i)[0], "Cumsum_Sec_Dim"
        ] = dict_subsum.get(i)[1]

    # calculate relative quantity
    df_grouped["Relative_numeric_dimension"] = (
        df_grouped["numeric_dimension"] / df_grouped["Cumsum_Sec_Dim"]
    )

    # calculate cumsum relative quantity (~y-axis in pareto chart)
    df_grouped["Cumsum_Relative_numeric_dimension"] = (
        df_grouped["Relative_numeric_dimension"]
        .groupby(df_grouped["secondary_dimension"])
        .cumsum()
    )

    # add relative primary & secondary dimension for visualization in (~x-axis in pareto chart)
    d_rel_primary_dimension = (
        df_grouped.groupby(df_grouped["secondary_dimension"])
        .apply(lambda x: 1 / len(x))
        .to_dict()
    )
    df_grouped["Relative_primary_dimension"] = df_grouped[
        "secondary_dimension"
    ].replace(d_rel_primary_dimension)

    df_grouped["Cumsum_Relative_primary_dimension"] = (
        df_grouped["Relative_primary_dimension"]
        .groupby(df_grouped["secondary_dimension"])
        .cumsum()
    )

    # prepare ABC classification thresholds and classes
    class_thresholds = [
        (df_grouped["Cumsum_Relative_numeric_dimension"] <= A),
        (
            (df_grouped["Cumsum_Relative_numeric_dimension"] > A)
            & (df_grouped["Cumsum_Relative_numeric_dimension"] <= B)
        ),
        (df_grouped["Cumsum_Relative_numeric_dimension"] > B),
    ]
    class_values = ["A", "B", "C"]

    # disagg secondary dimension to provided names
    df_grouped[secondary_dimensions] = df_grouped["secondary_dimension"].str.split(
        "-", expand=True
    )

    # assign classes
    df_grouped["Class"] = np.select(class_thresholds, class_values)

    # rename columns back to provided names
    columns_input = dict((v, k) for k, v in columns.items())
    df_grouped = df_grouped.rename(columns=columns_input)

    # clean output before return
    if classified_only:
        df_grouped = df_grouped.drop(
            columns=[
                #"Cumsum_Relative_numeric_dimension",
                "Relative_numeric_dimension",
                "Cumsum_Sec_Dim",
                #"Cumsum_Relative_numeric_dimension",
                "secondary_dimension",
                "Relative_primary_dimension",
                "Cumsum_Relative_primary_dimension",
            ]
        )

    return df_grouped
