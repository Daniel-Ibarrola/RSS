# Alerts (CAP)

CAP alerts (cap files) are stored in this directory.

## About CAP 


### Updating alerts

Whenever a CAP alert is changed, a new Alert (a new XML file) is issued. When this occurs, a new 
Atom feed <entry> or RSS feed <item> should be created that links to the new alert. A feed should 
not edit information in an already-issued CAP alert. This practice helps ensure that there’s a 
trailing record of changes to an alert.


## References

- [Cap validator](https://cap-validator.appspot.com/)
- [Cap for the web](https://docs.google.com/document/u/0/d/1J7bz05S6C1c5WvCd4m6f9asGoKqUpa2OUsaqx4SPKzM/pub)
- [Google public alerts](https://developers.google.com/public-alerts/guides/introduction)
- [Updating Alerts](https://docs.oasis-open.org/emergency-adopt/cap-feeds/v1.0/cn02/cap-feeds-v1.0-cn02.html#_Toc382489987)