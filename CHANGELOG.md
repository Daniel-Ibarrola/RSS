# Changelog

## v1.8.1 (30/10/2023)
- Added a trailing slash "/" to endpoints who didn't have it.


## v1.8.0 (30/10/2023)

- Created a flask blueprint for the alerts api. 
- Removed `GET /alerts/latest/`. The latest alert can be retrieved with the
endpoint `GET /alerts/{identifier}` with the identifier set to 'latest'
- Removed optional argument 'save' from `GET /alerts/{identifier}/cap/`. This endpoint
always returns the cap file in xml format.
- Restored `GET /cap/latest` and marked it as deprecated.

## v.1.7.0 (25/09/2023)
Renamed API endpoints and organized them by resource.
- Renamed ` POST /new_alert` to `POST /alerts/`.
- Renamed `GET /last_alert/` to  `GET /alerts/latest/`.
- Renamed `GET /cap/{identidier}` to `GET /alerts/{identifier}/cap/`. This endpoint takes
the optional argument 'save' that takes on the values 'true' or 'false'. If set to 'true' indicates
to download the cap file. Else, the cap files contents are returned as part of the JSON response.
- Removed `GET /cap_contents/{identifier}` as its now part of the `/alerts/{identifier}/cap/` endpoint.

## v1.6.0 (19/09/2023)

### API
The GET /alerts/ endpoint accepts multiple optional parameters that can be used as filters.
The following endpoints are now redundant and were removed:
- GET /alerts/dates/{date}. Get alerts by date.
- GET /regions/{region_name}. Get alerts by region.
- GET /states/{state_code}. Get alerts by state.

Date, region, state, and type can now be used as parameters with the GET /alerts/ endpoint.

Removed many obsolete methods from `rss.api.alert.Alert` model.

APIClient was updated with the new endpoints.

## v1.5.0 (18/09/2023)

### CLI
Some utilities are now available via the CLI tool and can be accessed more easily. Example:

```shell
cap write --date 2023-09-15T00:00:00 --states CDMX --region 41109 --file test.cap
```

The following utilities can be access via the CLI:
- **write**: Write a CAP file with the specified parameters.
- **post**: Post a new alert to the API
- **generate**: Generate new alerts and add them to the database. Can only be used in dev mode.
- **server**: Start the test server that generates samples alerts. This can be used to test the integration of the CAP generator with the API

## v1.4.0

### API
- New endpoint to get alerts by state.
- New endpoint to get alerts by region.
- List alert endpoint can filter by events and not events.
- Dates endpoint can get alerts in a given range

### Tests
- API test were moved to the integration folder.

## v1.3.2

### CLI
Post alert uses region code instead of name.

## v1.3.1

### CLI

New CLI tool, currently allows only to post new alerts to the API.

### API

- POST /new_alert endpoint returns the json of the new posted alert on success.

## v1.3.0

## Documentation

- Added JSON API documentation.
- Added region and states code table to documentation.

## Refactoring

- Removed duplicate code in API endpoints.
- New unit tests for alert model.

## API

- Added custom JSON errors to API

## v1.2.0

### CAP format updated

Updated CAP files format to comply with the newest specifications. The code has been updated
to generate CAPs with the new format. Also, the sample cap files in the feeds directory were updated.

### Bugfixes
Fixed issues regarding environment variables in production mode.

### Documentation
The documentation was restructured and updated with instructions to run the apps in docker
containers.

## v1.1.0

### Refactored
The cap generator main program as well as the services was refactored. Main changes
include the use of pysocklib `AbstractService` as an abstract base class for all services.
The `TCPClient` class was removed and the new `AlertsClient` class inherits from pysocklib
`Client`. 

### Dependencies
- Updated requests to 2.31.0. Previous version had security issues
- Added pysocklib to dependencies

### Continuous integration
- Added CI with GitHub actions

### Containerization
- Can run tests in container.
- Can start the api in production mode inside container.
- Can start the cap generator program in container.

## v1.0.0

### Cap Generator

The cap generator program has been updated with the following features:

- Can handle alerts from multiple states
- Alerts are stored in a database

### Cap API

A rest API to save and retrieve alerts has been created. This API is consumed by the CAP RSS website.

## v0.1.0

### Initial Release

First production release to newest SASMEX server. This version includes the following features:

- Automated writing of cap files when a seismic alert is triggered
- Cap files generated with app passes google validation.
- Update cap alerts when new data arrives.
- Write cap alerts for other seismic events (no seismic alert triggered).
- Cap alerts can be viewed trough SASMEX's website.

### Future plans

- Save alerts and events to database
- Consult previous cap files.

