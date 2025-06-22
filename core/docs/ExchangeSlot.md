# ExchangeSlot


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**position** | **int** |  | [optional] 
**item_id** | **int** |  | [optional] [default to -1]
**price** | **int** |  | [optional] [default to -1]
**quantity_transacted** | **int** |  | [optional] [default to -1]
**total_quantity** | **int** |  | [optional] [default to -1]
**state** | [**ExchangeSlotState**](ExchangeSlotState.md) |  | [optional] 

## Example

```python
from core.generated.gds.models.exchange_slot import ExchangeSlot

# TODO update the JSON string below
json = "{}"
# create an instance of ExchangeSlot from a JSON string
exchange_slot_instance = ExchangeSlot.from_json(json)
# print the JSON string representation of the object
print(ExchangeSlot.to_json())

# convert the object into a dict
exchange_slot_dict = exchange_slot_instance.to_dict()
# create an instance of ExchangeSlot from a dict
exchange_slot_from_dict = ExchangeSlot.from_dict(exchange_slot_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


