# API Documentation

## Table of Contents

- [Authentication](#authentication)
- [Open Data](#open-data)
- [Tokens](#tokens)
  - [Create a Token](#create-a-token)
  - [Remember a Token](#remember-a-token)
  - [Invalidate a Token](#invalidate-a-token)
  - [Check a Token](#check-a-token)
- [Properties](#properties)
  - [List All Houses](#list-all-houses)
  - [List My Houses](#list-my-houses)
  - [Get a Specific House](#get-a-specific-house)
- [Measurements](#measurements)
  - [Save a Single Measurement](#save-a-single-measurement)
  - [Save a Packet of Measurements](#save-a-packet-of-measurements)
  - [List Measurements](#list-measurements)
  - [Get Last Measurement](#get-last-measurement)

---

## Authentication

The API uses **token authentication**. Some endpoints also require username and password.

All authenticated requests must include the token in the headers:

```
Authorization: Token <your_token>
```

---

## Open Data

The collected data from the live station can be accessed publicly (no authentication required):

```
https://logs.tsaklidis.gr/api/open/measurement/list/
```

All filters documented in the [List Measurements](#list-measurements) section are also available on open endpoints.

---

## Tokens

### Create a Token

Create a new token. Default type is **expiring**. Persistent tokens are only allowed for specific users.

| Field       | Value                                          |
|-------------|------------------------------------------------|
| URL         | `/api/token/{expiring,persistent}/new/`        |
| Method      | `POST`                                         |
| Permissions | Authenticated by username and password         |

**Body:**
```json
{
  "username": "admin",
  "password": "1234",
  "token_name": "machine"
}
```

---

### Remember a Token

Retrieve a specific token key by its name.

| Field       | Value                                                     |
|-------------|-----------------------------------------------------------|
| URL         | `/api/token/remember/`                                    |
| Method      | `POST`                                                    |
| Permissions | Authenticated by username and password, must be token owner |

**Body:**
```json
{
  "username": "admin",
  "password": "1234",
  "token_name": "new"
}
```

---

### Invalidate a Token

Invalidate a specific token by name and key.

| Field       | Value                                                     |
|-------------|-----------------------------------------------------------|
| URL         | `/api/token/invalidate/`                                  |
| Method      | `POST`                                                    |
| Permissions | Authenticated by username and password, must be token owner |

**Body:**
```json
{
  "username": "admin",
  "password": "1234",
  "token_name": "new",
  "key": "34ferferfer"
}
```

---

### Check a Token

Check if a provided token is still valid.

| Field       | Value                                                     |
|-------------|-----------------------------------------------------------|
| URL         | `/api/token/check/`                                       |
| Method      | `POST`                                                    |
| Permissions | Authenticated by username and password, must be token owner |

**Body:**
```json
{
  "username": "admin",
  "password": "1234",
  "key": "34ferferfer"
}
```

---

## Properties

### List All Houses

List all houses and their spaces.

| Field       | Value                                  |
|-------------|----------------------------------------|
| URL         | `/api/house/all/`                      |
| Method      | `GET`                                  |
| Body        | None                                   |
| Permissions | Authenticated user and Administrator   |

---

### List My Houses

List all houses related to the authenticated user.

| Field       | Value                  |
|-------------|------------------------|
| URL         | `/api/house/my/`       |
| Method      | `GET`                  |
| Body        | None                   |
| Permissions | Authenticated user     |

---

### Get a Specific House

Get details of a specific house by its UUID.

| Field       | Value                                          |
|-------------|-------------------------------------------------|
| URL         | `/api/house/<uuid>/`                            |
| Method      | `GET`                                           |
| Body        | None                                            |
| Permissions | Authenticated by token, must be House Owner     |

---

## Measurements

### Save a Single Measurement

| Field       | Value                                          |
|-------------|-------------------------------------------------|
| URL         | `/api/measurement/new/`                         |
| Method      | `POST`                                          |
| Permissions | Authenticated by token, must be Space Owner     |

**Body:**
```json
{
  "space_uuid": "<space uuid>",
  "sensor_uuid": "<sensor uuid>",
  "value": 25.5
}
```

---

### Save a Packet of Measurements

Save multiple measurements in a single request.

| Field       | Value                                          |
|-------------|-------------------------------------------------|
| URL         | `/api/measurement/pack/new/`                    |
| Method      | `POST`                                          |
| Permissions | Authenticated by token, must be Space Owner     |

**Body:**
```json
[
  {"space_uuid": "<space uuid>", "sensor_uuid": "3cp", "value": 25},
  {"space_uuid": "bed5", "sensor_uuid": "t5c", "value": 26},
  {"space_uuid": "bed5", "sensor_uuid": "t5c", "value": 26, "custom_created_on": "2020-12-22 16:27:34"}
]
```

> **Note:** `custom_created_on` is optional. Use it to set a custom creation date for the measurement.

---

### List Measurements

Retrieve a paginated list of measurements with optional filters.

| Field       | Value                                          |
|-------------|-------------------------------------------------|
| URL         | `/api/measurement/list/`                        |
| Method      | `GET`                                           |
| Permissions | Authenticated by token, must be Space Owner     |

**Query Parameters:**

| Parameter      | Required | Description                                  |
|----------------|----------|----------------------------------------------|
| `space_uuid`   | Yes      | UUID of the space                            |
| `sensor_uuid`  | No       | UUID of the sensor                           |
| `latest_hours` | No       | If set, returns only measurements from the last N hours |
| `order_by`     | No       | One of: `created_on`, `-created_on`, `value`, `-value` |
| `limit`        | No       | Number of results per page                   |

**Available Date/Time Filters:**

| Filter              | Description                         |
|---------------------|-------------------------------------|
| `date__year`        | Exact year                          |
| `date__month`       | Exact month                         |
| `date__month__lte`  | Month less than or equal            |
| `date__month__lt`   | Month less than                     |
| `date__day`         | Exact day                           |
| `date__day__lte`    | Day less than or equal              |
| `date__day__lt`     | Day less than                       |
| `date__day__gte`    | Day greater than or equal           |
| `date__day__gt`     | Day greater than                    |
| `time__hour`        | Exact hour                          |
| `time__hour__lte`   | Hour less than or equal             |
| `time__hour__lt`    | Hour less than                      |
| `time__hour__gte`   | Hour greater than or equal          |
| `time__hour__gt`    | Hour greater than                   |

Filter order can be random. Omitting all filters returns all measurements.

**Example Request:**

```
/api/measurement/list/?space_uuid=dk8&sensor_uuid=0b4&date__month=9&date__day__gt=10&date__day__lt=20&time__hour__lte=18
```

This returns measurements for sensor `0b4` in space `dk8` where:
- Month is September (`date__month=9`)
- Day is greater than 10 (`date__day__gt=10`)
- Day is less than 20 (`date__day__lt=20`)
- Hour is before 18:00 (`time__hour__lte=18`)

**Response:**
```json
{
  "count": 6941,
  "next": "https://logs.tsaklidis.gr/api/measurement/list/?page=2",
  "previous": null,
  "results": [
    {
      "created_on": "2019-09-01 00:00:06",
      "value": 38.2
    }
  ]
}
```

| Field      | Description                                                 |
|------------|-------------------------------------------------------------|
| `count`    | Total number of results across all pages                    |
| `next`     | URL of the next page (`null` if on the last page)           |
| `previous` | URL of the previous page (`null` if on the first page)      |
| `results`  | Array of measurement objects for the current page           |

---

### Get Last Measurement

Get the most recent measurement for a given sensor. Useful for widgets and dashboards.

| Field       | Value                                          |
|-------------|-------------------------------------------------|
| URL         | `/api/measurement/list/last/`                   |
| Method      | `GET`                                           |
| Permissions | Authenticated by token, must be Space Owner     |

**Query Parameters:**

| Parameter      | Required | Description                |
|----------------|----------|----------------------------|
| `space_uuid`   | Yes      | UUID of the space          |
| `sensor_uuid`  | Yes      | UUID of the sensor         |

**Example:**
```
/api/measurement/list/last/?space_uuid=dk8&sensor_uuid=9bd60
```

> **Open endpoint** (no authentication required):
> ```
> /api/open/measurement/list/last/?sensor_uuid=9bd60
> ```
