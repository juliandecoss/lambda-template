from re import findall
from typing import Any


def camel_case_dict(dictionary: dict) -> dict:
    return transform_case_style_dict(dictionary, "camelCase")


def snake_case_dict(dictionary: dict) -> dict:
    return transform_case_style_dict(dictionary, "snake_case")


def transform_case_style_dict(dictionary: dict, to_case_style: str) -> dict:
    new_dict = {}
    for key, value in dictionary.items():
        if isinstance(value, dict):
            value = transform_case_style_dict(value, to_case_style)
        new_dict[key.replace(key, transform_case_style(key, to_case_style))] = value
    return new_dict


def transform_case_style(string: str, to_case_style: str) -> str:
    transformed_string = string
    if "camel" in to_case_style:
        if string.startswith("_"):
            return string[1:]
        splitted = string.split("_")
        subsequent_words = "".join(
            sub_string.capitalize() for sub_string in splitted[1:]
        )
        transformed_string = f"{splitted[0]}{subsequent_words}"
    elif "snake" in to_case_style:
        string = string.lower() if string.isupper() else string
        splitted = findall(r"[A-Za-z][a-z0-9]*", string)
        if splitted and len(splitted) > 1:
            subsequent_words = "_".join(
                sub_string.lower() for sub_string in splitted[1:]
            )
            transformed_string = "_".join([splitted[0].lower(), subsequent_words])
    return transformed_string


def get_case_insensitive_key(dictionary: dict, key: str, default: Any = None) -> Any:
    if isinstance(dictionary, dict):
        for k in [key.lower(), key.capitalize(), key.upper()]:
            if k in dictionary:
                return dictionary[k]
    return default
