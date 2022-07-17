## 5.4.0 (2022-07-17)

### Feat

- add destination stop in estimations

## 5.3.1 (2022-01-14)

### Fix

- **service**: fix route_ways generation in all_stops
- **service**: fix route_ways generation in all_stops

## 5.3.0 (2021-12-27)

### Feat

- **entrypoints**: api vehicle route_way required

## 5.2.0 (2021-12-18)

### Fix

- allow null vehicle id and/or name

### Feat

- **entrypoints**: add new stop and route examples

### Refactor

- **service**: remove unused functions

## 5.1.0 (2021-12-17)

### Feat

- **service**: disable cache in stop service
- **service**: disable cache in route_service

## 5.0.1 (2021-12-14)

### Perf

- **entrypoints**: dont validate cache
- **entrypoints**: dont validate cache

## 5.0.0 (2021-12-13)

### Feat

- **entrypoints**: handle stop or route not found
- **entrypoints**: add response models and cache to route endpoints
- **entrypoints**: enable cache for stop endpoints
- add response model for stop related endpoints

### Fix

- **entrypoints**: add request and response

### Perf

- **service**: retry get_json also on HTTP status

### BREAKING CHANGE

- Removed exclude parameter and changed response format.

## 4.5.0 (2021-12-12)

### Feat

- add route endpoints

## 4.4.0 (2021-12-11)

### Feat

- **service**: include line code in estimations

## 4.3.2 (2021-12-11)

### Fix

- **madrid**: set correct line id on estimations

## 4.3.1 (2021-12-11)

### Fix

- **service**: handle upstream city api errors

## 4.3.0 (2021-12-11)

### Feat

- **madrid**: support all transport types

## 4.2.0 (2021-12-10)

### Feat

- **service**: get transport type from city API estimations

### Fix

- **domain**: fix transport type enum duplicated value

### Perf

- **entrypoints**: user orjson for faster serialization

## 4.1.0 (2021-12-07)

### Feat

- **service**: iclude line ways in stop info

## 4.0.0 (2021-12-07)

### Fix

- **madrid.py**: type error

### Feat

- add lines info to stop
- stops as dictionary

## 3.2.0 (2021-11-07)

### Feat

- set env vars defaults and refactor

## 3.1.0 (2021-11-06)

### Feat

- all city stops endpoint

## 3.0.0 (2021-11-06)

### Feat

- **api**: add stop info entrypoint
- **service**: get stop info

### Refactor

- **api**: refactor endpoints

## 2.3.0 (2021-09-21)

### Feat

- **data**: database module with postgres implementation

## 2.2.1 (2021-09-20)

### Perf

- **service**: manually convert dataclasses to dict

## 2.2.0 (2021-09-16)

### Feat

- **entrypoints**: api title, description and root path

## 2.1.1 (2021-09-13)

### Perf

- **service**: change fetch timeout and retries for external apis

### Refactor

- Add service layer

## 2.1.0 (2021-09-10)

### Refactor

- changed name to now8-api
- initial structure

### Feat

- **logic**: get_estimations
- **data**: madrid intercity buses get estiamtions
