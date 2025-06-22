# LiveConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**autotrader_on** | **bool** |  | [optional] 
**top_level_config** | [**TopLevelConfig**](TopLevelConfig.md) |  | [optional] 
**strat_configs** | [**List[StratConfig]**](StratConfig.md) |  | [optional] 

## Example

```python
from core.generated.gds.models.live_config import LiveConfig

# TODO update the JSON string below
json = "{}"
# create an instance of LiveConfig from a JSON string
live_config_instance = LiveConfig.from_json(json)
# print the JSON string representation of the object
print(LiveConfig.to_json())

# convert the object into a dict
live_config_dict = live_config_instance.to_dict()
# create an instance of LiveConfig from a dict
live_config_from_dict = LiveConfig.from_dict(live_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


