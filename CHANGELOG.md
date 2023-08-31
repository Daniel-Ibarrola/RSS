# Changelog

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

