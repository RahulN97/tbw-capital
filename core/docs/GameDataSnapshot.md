# GameDataSnapshot


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**session** | [**Session**](Session.md) |  | [optional] 
**exchange** | [**Exchange**](Exchange.md) |  | [optional] 
**inventory** | [**Inventory**](Inventory.md) |  | [optional] 
**player** | [**Player**](Player.md) |  | [optional] 
**chat_box** | [**ChatBox**](ChatBox.md) |  | [optional] 
**creation_time** | **int** |  | [optional] 

## Example

```python
from core.generated.gds.models.game_data_snapshot import GameDataSnapshot

# TODO update the JSON string below
json = "{}"
# create an instance of GameDataSnapshot from a JSON string
game_data_snapshot_instance = GameDataSnapshot.from_json(json)
# print the JSON string representation of the object
print(GameDataSnapshot.to_json())

# convert the object into a dict
game_data_snapshot_dict = game_data_snapshot_instance.to_dict()
# create an instance of GameDataSnapshot from a dict
game_data_snapshot_from_dict = GameDataSnapshot.from_dict(game_data_snapshot_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


