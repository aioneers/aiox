import aiox
import numpy as np
import pandas as pd


def test_create_time_series():
    df = pd.DataFrame()

    # create time-series with defined distribution
    for i in range(100):
        quantities = aiox.create_time_series(
            distribution="normal",
            p_mean=1000,
            p_std=300,
            num_periods=12,
            periodicity="M",
            start_date="2020-01-01",
            actual_material_number=str("{:04d}".format(np.random.randint(1000)))
            + str("-")
            + str("{:02d}".format(np.random.randint(20)))
            + str("-")
            + str("{:05d}".format(np.random.randint(5))),
            standard_price=1,
            intermittency=0.2,
        )
        df = df.append(quantities)

    assert len(df) == 100 * 12
    print(len(df))