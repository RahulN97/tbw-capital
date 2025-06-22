# core.generated.gds.GdsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**chat_get**](GdsApi.md#chat_get) | **GET** /chat | Get Chat Box Data
[**config_get**](GdsApi.md#config_get) | **GET** /config | Get Live Config
[**exchange_get**](GdsApi.md#exchange_get) | **GET** /exchange | Get Exchange Data
[**health_get**](GdsApi.md#health_get) | **GET** /health | Health Check
[**inventory_get**](GdsApi.md#inventory_get) | **GET** /inventory | Get Inventory Data
[**player_get**](GdsApi.md#player_get) | **GET** /player | Get Player Data
[**session_get**](GdsApi.md#session_get) | **GET** /session | Get Session Data
[**snapshot_get**](GdsApi.md#snapshot_get) | **GET** /snapshot | Get Game Data Snapshot


# **chat_get**
> ChatBox chat_get()

Get Chat Box Data

### Example


```python
import core.generated.gds
from core.generated.gds.models.chat_box import ChatBox
from core.generated.gds.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = core.generated.gds.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with core.generated.gds.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = core.generated.gds.GdsApi(api_client)

    try:
        # Get Chat Box Data
        api_response = api_instance.chat_get()
        print("The response of GdsApi->chat_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GdsApi->chat_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ChatBox**](ChatBox.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Current chat box contents |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **config_get**
> LiveConfig config_get()

Get Live Config

### Example


```python
import core.generated.gds
from core.generated.gds.models.live_config import LiveConfig
from core.generated.gds.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = core.generated.gds.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with core.generated.gds.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = core.generated.gds.GdsApi(api_client)

    try:
        # Get Live Config
        api_response = api_instance.config_get()
        print("The response of GdsApi->config_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GdsApi->config_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**LiveConfig**](LiveConfig.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Current live configuration |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **exchange_get**
> Exchange exchange_get()

Get Exchange Data

### Example


```python
import core.generated.gds
from core.generated.gds.models.exchange import Exchange
from core.generated.gds.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = core.generated.gds.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with core.generated.gds.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = core.generated.gds.GdsApi(api_client)

    try:
        # Get Exchange Data
        api_response = api_instance.exchange_get()
        print("The response of GdsApi->exchange_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GdsApi->exchange_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Exchange**](Exchange.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Current exchange data |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **health_get**
> Health health_get()

Health Check

### Example


```python
import core.generated.gds
from core.generated.gds.models.health import Health
from core.generated.gds.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = core.generated.gds.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with core.generated.gds.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = core.generated.gds.GdsApi(api_client)

    try:
        # Health Check
        api_response = api_instance.health_get()
        print("The response of GdsApi->health_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GdsApi->health_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Health**](Health.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Server is healthy |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **inventory_get**
> Inventory inventory_get()

Get Inventory Data

### Example


```python
import core.generated.gds
from core.generated.gds.models.inventory import Inventory
from core.generated.gds.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = core.generated.gds.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with core.generated.gds.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = core.generated.gds.GdsApi(api_client)

    try:
        # Get Inventory Data
        api_response = api_instance.inventory_get()
        print("The response of GdsApi->inventory_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GdsApi->inventory_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Inventory**](Inventory.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Current inventory data |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **player_get**
> Player player_get()

Get Player Data

### Example


```python
import core.generated.gds
from core.generated.gds.models.player import Player
from core.generated.gds.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = core.generated.gds.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with core.generated.gds.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = core.generated.gds.GdsApi(api_client)

    try:
        # Get Player Data
        api_response = api_instance.player_get()
        print("The response of GdsApi->player_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GdsApi->player_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Player**](Player.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Current player data |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **session_get**
> Session session_get()

Get Session Data

### Example


```python
import core.generated.gds
from core.generated.gds.models.session import Session
from core.generated.gds.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = core.generated.gds.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with core.generated.gds.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = core.generated.gds.GdsApi(api_client)

    try:
        # Get Session Data
        api_response = api_instance.session_get()
        print("The response of GdsApi->session_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GdsApi->session_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Session**](Session.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Current session information |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **snapshot_get**
> GameDataSnapshot snapshot_get()

Get Game Data Snapshot

### Example


```python
import core.generated.gds
from core.generated.gds.models.game_data_snapshot import GameDataSnapshot
from core.generated.gds.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = core.generated.gds.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with core.generated.gds.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = core.generated.gds.GdsApi(api_client)

    try:
        # Get Game Data Snapshot
        api_response = api_instance.snapshot_get()
        print("The response of GdsApi->snapshot_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GdsApi->snapshot_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GameDataSnapshot**](GameDataSnapshot.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A snapshot of the game data |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

