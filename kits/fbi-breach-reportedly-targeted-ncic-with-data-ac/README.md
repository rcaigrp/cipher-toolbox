# FBI NCIC Breach Defense Kit

This kit provides defensive measures for the reported FBI breach targeting the National Crime Information Center (NCIC) database. The threat involves potential unauthorized access to sensitive law enforcement data, with unconfirmed reports of data access or modification.

## Who is Exposed
Organizations that maintain access to NCIC systems, particularly those with:
- Law enforcement databases
- CJIS (Criminal Justice Information Services) compliance requirements
- Systems handling sensitive criminal justice information

## Files in this Kit
- `detection/`: Detection rules for logs, memory, network, and hunting queries
- `check_exposure.py`: Checks if this machine is exposed to NCIC-related risks
- `mitigate.py`: Hardening measures and workarounds (dry-run by default)