# Quarantine

Quarantine workloads exhibiting anomalous behavior.

## What it does

This feature watches your Halo events stream for specific events from specific
workload groups.  When these events are observed, the target workload is moved
into a quarantine group in Halo, which isolates the workload until a security
engineer can perform a forensic analysis.  When a quarantine event is
triggered, a message to this effect will appear in Slack.

## Configuration

This feature does not run by default, and requires additional setup before it
can be enabled.  The configuration for this feature is delivered via environment
variables:

| Variable                             | Purpose                                                                   |
|--------------------------------------|---------------------------------------------------------------------------|
| QUARANTINE_ENABLED                   | Set to `True` or `true` to enable quarantine.                             |
| QUARANTINE_TRIGGER_GROUP_NAMES       | Comma-separated list of groups for qualifying events for quarantine.      |
| QUARANTINE_GROUP_NAME                | Name of Halo server group to be used as quarantine.                       |
| QUARANTINE_TRIGGER_EVENTS            | Comma-separated list of event types for qualifying quarantine events.     |
| QUARANTINE_TRIGGER_ONLY_ON_CRITICAL  | Set to `True` or `true` to qualify only critical events for quarantine.   |


## Qualification

Quarantine uses a process for qualifying events before triggering a quarantine
action.  The following criteria must be met before a workload is quarantined:

* Event qualifications:
    * Event must match one of the event types defined by `QUARANTINE_TRIGGER_EVENTS`.
    * If `QUARANTINE_TRIGGER_ONLY_ON_CRITICAL` is set to `True` or `true`, Halo event must be critical.
    * Workload triggering event must belong to a group named in `QUARANTINE_TRIGGER_GROUP_NAMES`.
* Environmental qualifications:
    * Group names must be unambiguous.  Exactly one group for each of `QUARANTINE_TRIGGER_GROUP_NAMES` and `QUARANTINE_GROUP_NAME` must exist.  If zero or more than one group match (by name) exists in the Halo account, the event will not trigger a quarantine action.  This check is performed every time an event is qualified.
* Configuration qualification:
    * If any variable listed above fails validation or is empty, the Quarantine feature will be disabled.
