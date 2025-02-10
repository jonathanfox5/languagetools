"""Extract IPA information from a wiktionary dump from kaikki.org"""

__author__ = "Jonathan Fox"
__copyright__ = "Copyright 2024, Jonathan Fox"
__license__ = "GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html"

from pathlib import Path
from typing import Any

import openpyxl  # noqa Needs to be installed but not referenced in script
import pandas as pd

INPUT_DICT = "dict.jsonl"
OUTPUT_SHEET = "ita_ipa.xlsx"
LANG_CODE = "it"
COLUMNS = ["word", "pos_title", "sounds"]
SORT_ON_COLUMNS = ["word", "pos_title"]


def read_jsonl(file_path: Path) -> pd.DataFrame:
    """Read jsonl to a pandas dataframe"""
    df = pd.read_json(file_path, lines=True)

    return df


def select_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Pull out specific columns from a dataframe"""
    df = df[columns]

    return df


def filter_df(df: pd.DataFrame, field: str, search_term: Any) -> pd.DataFrame:
    """Filter a single column by the value of a single field"""
    df = df[df[field] == search_term]

    return df


def sort_df(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Sort a dataframe by a list of columns in ascending order"""
    df = df.sort_values(by=columns)

    return df


def extract_ipa(x) -> str:
    """Extract IPA from the "sounds" field"""
    try:
        ipa = x[0]["ipa"]

        return ipa
    except (ValueError, IndexError, TypeError, AttributeError, KeyError):
        return ""


def main():
    """Main function to extract IPA from a wiktionary dump"""

    # Read in the json
    print("~~~ Reading data ~~~")
    df = read_jsonl(Path(INPUT_DICT))

    # Select only the data that we need
    print("~~~ Processing data ~~~")
    df = filter_df(df, "lang_code", LANG_CODE)
    df = select_columns(df, COLUMNS)

    # Grab the IPA from its data structure
    df["sounds"] = df["sounds"].apply(extract_ipa)

    # Sort for ease of use
    df = sort_df(df, SORT_ON_COLUMNS)

    # Save to Excel (specifically to Excel to avoid compatibility issues with csv character encoding)
    print("~~~ Writing data ~~~")
    df.to_excel(Path(OUTPUT_SHEET), index=False)

    print("~~~ Done ~~~")


if __name__ == "__main__":
    main()
