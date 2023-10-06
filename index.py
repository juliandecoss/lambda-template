from src.app import main


def handler(event: dict, context) -> dict:
    return main(event, context)