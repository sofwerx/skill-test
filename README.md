# tsa-wait-skill

This skill uses the following 2 API's:

The TSA wait times API: http://apps.tsa.dhs.gov/MyTSAWebService/GetTSOWaitTimes.ashx which is documented at https://www.dhs.gov/mytsa-api-documentation

The IATA Codes api located at https://iatacodes.org/

Using this information we get the last TSA wait time for an airport code and use the IATA api to get the full name of the airport to respond back with the wait time.

To get this done we need:
   - requests module installed via msm when you install the skill, if it doesn't install it can be installed via `pip install requests`

# Setup API
Go to https://iatacodes.org/ and get a free api_key, put that key into your /etc/mycroft/mycroft.conf file in order for it to work.

Example:

```
"TsaWaitSkill": {
    "airport_api_key"
  }
```

# Installing
you can install this via msm install https://github.com/btotharye/tsa-wait-skill.git

## Current state

Working features:
  - what is the tsa wait for RDU (or any other airport code)
  - what is the tsa wait at RDU (or any other airport code)
  - how long is the tsa wait at RDU (or any other airport code)

Known issues:
 - ...

TODO:
 - add in fuzzy matching for airport name given and get code for wait time
