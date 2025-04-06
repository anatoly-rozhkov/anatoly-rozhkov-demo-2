from typing import Any


async def validate_iterable_objects(response_dict, object_list: Any, individual_serializer: Any):
    for index, response_dict_item in enumerate(response_dict):
        expected_result = object_list[index]

        await individual_serializer(response_dict_item, expected_result)
