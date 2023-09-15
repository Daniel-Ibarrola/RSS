# Changelog

## v1.4.1

### CLI
Post alert uses region code instead of name.

## v1.4.0

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

