# from datetime import datetime
# from os import environ

# from boto3 import resource


# def get_dynamo_resource() -> resource:
#     return resource("dynamodb", endpoint_url=environ["DYNAMO_ENDPOINT_URL"])


# def put_item(table_name: str, values: dict) -> None:
#     dynamodb = get_dynamo_resource()
#     table = dynamodb.Table(table_name)
#     values["CreationDate"] = str(datetime.now()).split(".")[0]
#     table.put_item(Item=values)


# def get_items(table_name: str) -> list:
#     dynamodb = get_dynamo_resource()
#     table = dynamodb.Table(table_name)
#     return table.scan()["Items"]
