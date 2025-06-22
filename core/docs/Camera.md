# Camera


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**z** | **int** |  | [optional] 
**yaw** | **int** |  | [optional] 
**scale** | **int** |  | [optional] 

## Example

```python
from core.generated.gds.models.camera import Camera

# TODO update the JSON string below
json = "{}"
# create an instance of Camera from a JSON string
camera_instance = Camera.from_json(json)
# print the JSON string representation of the object
print(Camera.to_json())

# convert the object into a dict
camera_dict = camera_instance.to_dict()
# create an instance of Camera from a dict
camera_from_dict = Camera.from_dict(camera_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


