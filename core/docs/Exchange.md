# Exchange


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**slots** | [**List[ExchangeSlot]**](ExchangeSlot.md) |  | [optional] 

## Example

```python
from core.generated.gds.models.exchange import Exchange

# TODO update the JSON string below
json = "{}"
# create an instance of Exchange from a JSON string
exchange_instance = Exchange.from_json(json)
# print the JSON string representation of the object
print(Exchange.to_json())

# convert the object into a dict
exchange_dict = exchange_instance.to_dict()
# create an instance of Exchange from a dict
exchange_from_dict = Exchange.from_dict(exchange_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


