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
]
-permissions: Authenticated users by token and Space Owners
```



## List all measurements

```code
-url: /api/measurement/list/all/
-method: GET
-body: {"space_uuid": "sde3", "sensor_uuid":"s45t"}
-permissions: Authenticated users by token and Space Owners
```




