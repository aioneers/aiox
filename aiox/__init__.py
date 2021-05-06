from .abc_analysis import abc_analysis

from .xyz_analysis import xyz_analysis

from .create_time_series import create_time_series


from aioconnect.azure_key_vault import _vault_set_dbutils


from .read_and_write import read_and_write, read_and_write_all, read_and_concat, read_all_sheets


def set_dbutils(dbutils_var):
    """Allows the vault functions to use the ``dbutils`` variable

    Parameters
    ----------
        dbutils_var
            ``dbutils`` variable from Databricks should be passed here
    """
    _vault_set_dbutils(dbutils_var)
