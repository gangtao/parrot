the parrot is a python tools that convert the existing splunk eventgen conf into a new json model that can be used by any other programming language to generate events.

the JSON model scheme contains:
- name
- patterns

the patterns is a list of `pattern` with scheme that contains:
- name
- earliest
- latest
- pattern
- value

the `pattern` scheme cotains:
- end
- start
- value
- token

the `token` scheme contains
- id
- replacement
- replacement_values
- type
- value

