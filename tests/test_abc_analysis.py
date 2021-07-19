import numpy as np
import aiox
import pandas as pd


class Test_abc_analysis:

    def test_w_multiple_dimensions(self):
        # create sample data
        products, quantities, countries, regions, cities = {}, {}, {}, {}, {}
        np.random.seed(seed=0)
        for i in range(1000):
            products[i] = "{:04d}".format(np.random.randint(15))
            quantities[i] = np.random.randint(1000)
            countries[i] = "{:03d}".format(np.random.randint(4))
            regions[i] = "{:05d}".format(np.random.randint(3))
            cities[i] = "{:02d}".format(np.random.randint(2))
        # prepare sample data DataFrame
        df = pd.DataFrame()
        df["Product"] = products.values()
        df["Country"] = countries.values()
        df["Quantity"] = quantities.values()
        df["Region"] = regions.values()
        df["City"] = cities.values()

        results = aiox.abc_analysis(
            df,
            primary_dimension="Product",
            secondary_dimensions=["Country", "Region", "City"],
            numeric_dimension="Quantity",
        )

        results[
            (results["secondary_dimension"] == "003-00002-01")
            | (results["secondary_dimension"] == "003-00002-00")
        ]
        assert len(results)

    def test_wo_additional_dimensions(self):
        # create sample data
        products, quantities = {}, {}
        np.random.seed(seed=0)
        for i in range(1000):
            products[i] = "{:04d}".format(np.random.randint(15))
            quantities[i] = np.random.randint(1000)
        # prepare sample data DataFrame
        df = pd.DataFrame()
        df["Product"] = products.values()
        df["Quantity"] = quantities.values()

        results = aiox.abc_analysis(
            df, primary_dimension="Product", numeric_dimension="Quantity"
        )

        assert len(results)

    def test_wo_additional_dimensions_w_typo(self):
        # create sample data
        products, quantities = {}, {}
        np.random.seed(seed=0)
        for i in range(1000):
            products[i] = "{:04d}".format(np.random.randint(15))
            quantities[i] = np.random.randint(1000)
        # prepare sample data DataFrame
        df = pd.DataFrame()
        df["Product"] = products.values()
        df["Quantity"] = quantities.values()

        try:
            aiox.abc_analysis(
                df, primary_dimension="Product", numeric_dimension="Quansdkhfjksdhfk"
            )
        except KeyError:
            assert True
        else:
            assert False

    def test_w_multiple_dimensions_w_typos(self):
        # create sample data
        products, quantities, countries, regions, cities = {}, {}, {}, {}, {}
        np.random.seed(seed=0)
        for i in range(1000):
            products[i] = "{:04d}".format(np.random.randint(15))
            quantities[i] = np.random.randint(1000)
            countries[i] = "{:03d}".format(np.random.randint(4))
            regions[i] = "{:05d}".format(np.random.randint(3))
            cities[i] = "{:02d}".format(np.random.randint(2))
        # prepare sample data DataFrame
        df = pd.DataFrame()
        df["Product"] = products.values()
        df["Country"] = countries.values()
        df["Quantity"] = quantities.values()
        df["Region"] = regions.values()
        df["City"] = cities.values()

        try:
            results = aiox.abc_analysis(
                df,
                primary_dimension="Product",
                secondary_dimensions=[
                    "Coundfhjshdf", "Regdsfkshf", "Cidfhsdfj"],
                numeric_dimension="Quantity",
            )

            results[
                (results["secondary_dimension"] == "003-00002-01")
                | (results["secondary_dimension"] == "003-00002-00")
            ]
        except KeyError:
            assert True
        else:
            assert False

    # def test_w_unnecessary_dimensions(self):
    #     # create sample data
    #     products, quantities, countries, regions, cities = {}, {}, {}, {}, {}
    #     np.random.seed(seed=0)
    #     for i in range(1000):
    #         products[i] = "{:04d}".format(np.random.randint(15))
    #         quantities[i] = np.random.randint(1000)
    #         countries[i] = "{:03d}".format(np.random.randint(4))
    #         regions[i] = "{:05d}".format(np.random.randint(3))
    #         cities[i] = "{:02d}".format(np.random.randint(2))
    #     # prepare sample data DataFrame
    #     df = pd.DataFrame()
    #     df["Product"] = products.values()
    #     df["Country"] = countries.values()
    #     df["Quantity"] = quantities.values()
    #     df["Region"] = regions.values()
    #     df["City"] = cities.values()

    #     results = aiox.abc_analysis(
    #         df,
    #         primary_dimension="Product",
    #         secondary_dimensions=["Country", "Region"],
    #         numeric_dimension="Quantity",
    #     )

    #     results[
    #         (results["secondary_dimension"] == "003-00002-01")
    #         | (results["secondary_dimension"] == "003-00002-00")
    #     ]
    #     assert len(results)
