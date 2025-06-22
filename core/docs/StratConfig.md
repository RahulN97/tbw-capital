# StratConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**strat_type** | **str** |  | 
**activated** | **bool** |  | [optional] 
**wait_duration** | **int** |  | [optional] 
**max_offer_time** | **int** |  | [optional] 

## Example

```python
from core.generated.gds.models.strat_config import StratConfig

# TODO update the JSON string below
json = "{}"
# create an instance of StratConfig from a JSON string
strat_config_instance = StratConfig.from_json(json)
# print the JSON string representation of the object
print(StratConfig.to_json())

# convert the object into a dict
strat_config_dict = strat_config_instance.to_dict()
# create an instance of StratConfig from a dict
strat_config_from_dict = StratConfig.from_dict(strat_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


