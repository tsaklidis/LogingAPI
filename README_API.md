## Open data
The collected data from live station can be accessed from the open API
 endpoints:

```code
https://logs.tsaklidis.gr/api/open/measurement/list/
```
All documented filters from the 'Measurements' section are also available

##

The api is based on token authentication and for some requests username and password.

All requests must have in headers Authorization: Token 'the_token'

##  Tokens
Create new token
Default token type is expiring, persistent tokens are allowed to specific users. <br>

```code
-url: /api/token/{expiring-persistent}/new/
-method: POST
-body: {"username":"admin","password":"1234", "token_name":"machine"}
-permissions: Authenticated by username and password
```


## Remember a valid token

```code
-method: POST
-body: {"username":"admin","password":"1234", "token_name":"new"}
-url: api/token/remember/
-permissions: Authenticated by username and password also token owner
``` 



## Invalidate a token

```code
-url: /api/token/invalidate/
-method: POST
-body: {"username":"admin","password":"1234", "token_name":"new", "key":"34ferferfer"}
-permissions: Authenticated by username and password also token owner

```


## Check if a token is valid

```code
-url: /api/token/check/
-method: POST
-body: {"username":"admin","password":"1234", "key":"34ferferfer"}
-permissions: Authenticated by username and password also token owner

```

## Properties

List all houses and their spaces

```code
-url: /api/house/all/
-method: GET
-body: None
-permissions: Authenticated user and Administrator

```



## List all houses related to user

```code
-url: /api/house/my/
-method: GET
-body: None
-permissions: Authenticated user

```



## List the requested house by uuid

```code
-url: /api/house/<uuid>/
-method: GET
-body: None
-permissions: Authenticated users by token and House Owner

```


## Measurements
Save a single measurement

```code
-url: /api/measurement/new/
-method: POST
-body: {"space_uuid":"{the uuid of space}","sensor_uuid":"{the uuid of sensor}", "value": {the value}}
-permissions: Authenticated users by token and Space Owners
```



## Save a packet of measurements

```code
-url: /api/measurement/pack/new/
-method: POST
-body:
[
	{"space_uuid":"{the uuid of space}","sensor_uuid":"3cp", "value": {the value}},
   	{"space_uuid":"bed5","sensor_uuid":"t5c", "value":26},
    {"space_uuid":"bed5","sensor_uuid":"t5c", "value":26, "custom_created_on": "2020-12-22 16:27:34"},
]
-notes: custom_created_on is optional in order to set custom creation date
-permissions: Authenticated users by token and Space Owners
```



## List measurements

```code
-url: /api/measurement/list/
-method: GET
-GET Arguments: {"space_uuid": "sde3", "sensor_uuid":"s45t"}
-permissions: Authenticated users by token and Space Owners
-filter_fields = (
    'date__day', 'date__month',
    'date__day__lte', 'date__day__lt',
    'date__day__gte', 'date__day__gt',
    'date__month__lte', 'date__month__lt',
    'time__hour',
    'time__hour__lte', 'time__hour__lt',
    'time__hour__gte', 'time__hour__gt',
)

```

-Example request with body:
```code
body = {
	"space_uuid": "dk8", "sensor_uuid":"0b4",
	"date__month":9, 
	"date__day__gt":10, "date__day__lt":20,
	"time__hour__lte":18
}
Final URL: /api/measurement/list/?space_uuid=dk8&sensor_uuid=0b4&date__month=9
&date__day__lt=20&time__hour__lte=18

```
-Returns measurements for sensor with uuid==0b4 which is placed in space with uuid==dk8  
but **only** measurements saved on 9th month (September) **and**  from day greater than 10 **and** day less than 20  
**and** before 18:00 o'clock
Filters order can be random. No filters returns all measurements

-Result body is

```code
"count": 6941,
"next": "https://logs.tsaklidis.gr/api/measurement/list/?page=2",
"previous": null,
"results": [
    {
        "created_on": "2019-09-01 00:00:06",
        "value": 38.2
    },
]
```

count: The total count of results  
next: The next page with the rest of results. If it is null, you are on last page.  
previous: If null you are on first page else previus page link


## Get las measurements
-This endpoint is useful for widgets