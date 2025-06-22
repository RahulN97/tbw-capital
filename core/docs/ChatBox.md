# ChatBox


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**messages** | [**List[Message]**](Message.md) |  | [optional] 

## Example

```python
from core.generated.gds.models.chat_box import ChatBox

# TODO update the JSON string below
json = "{}"
# create an instance of ChatBox from a JSON string
chat_box_instance = ChatBox.from_json(json)
# print the JSON string representation of the object
print(ChatBox.to_json())

# convert the object into a dict
chat_box_dict = chat_box_instance.to_dict()
# create an instance of ChatBox from a dict
chat_box_from_dict = ChatBox.from_dict(chat_box_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


