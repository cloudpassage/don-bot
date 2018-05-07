# IP Blocker

Manage an IP rolling blacklist (RBL) based on Halo events

## What it does

This feature monitors your Halo account, looking for specific events.  If an
event meets criteria, the tool will attempt to extract an IP address from
the event and place the IP address in a named IP Zone in your Halo account.
In one hour, the IP address will be removed from the IP RBL. This IP RBL may be
used throughout your Halo account, inside firewall orchestration policies.

## Configuration

This feature does not run by default, and requires additional setup before it
can be enabled.  The configuration for this feature is delivered via environment
variables:

| Variable                             | Purpose                                                                 |
|--------------------------------------|-------------------------------------------------------------------------|
| IPBLOCKER_ENABLED                    | Set to `True` or `true` to enable IP blocker.                           |
| IPBLOCKER_IP_ZONE_NAME               | Name of Halo IP zone to be managed by IP Blocker.                       |
| IPBLOCKER_TRIGGER_EVENTS             | Halo event types to trigger IP Blocker.                                 |
| IPBLOCKER_TRIGGER_ONLY_ON_CRITICAL   | Set to `True` or `true` to trigger IP Blocker only for critical events. |



## Qualification

IP Blocker uses a process for qualifying events before triggering an update to
the IP RBL. The following criteria must be met:

* Event qualifications:
    * Event must match one of the event types defined by `IPBLOCKER_TRIGGER_EVENTS`.
    * If `IPBLOCKER_TRIGGER_ONLY_ON_CRITICAL` is set to `True` or `true`, Halo event must be critical.
* Environmental qualifications:
    * IP zone name indicated in `IPBLOCKER_IP_ZONE_NAME` must exist.
* Configuration qualification:
    * If any variable listed above fails validation or is empty, the IP Blocker feature will be disabled.
