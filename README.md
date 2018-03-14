the parrot is a python tools that convert the existing splunk eventgen conf into a new json model that can be used by any other programming language to generate events.

the JSON model scheme contains:
- name : name of the model
- patterns : patterns contained in this model
- replacement : all the replacement values for file and mvfile

the patterns is a list of `pattern` with scheme that contains:
- name
- earliest
- latest
- pattern
- value
- source
- sourcetype
- perDayVolume

the `pattern` scheme cotains:
- start
- end
- value
- token : token field will exist in case there is a requirement to generate new values for this token, otherwise, it is a fixed value

the `token` scheme contains
- id
- replacement
- replacement_values
- type : timestamp|mvfile|file|random
- value

a sample token with a random replacement value:
`
{
	'start': 113,
	'token': {
		'replacement_values': [],
		'type': 'random',
		'id': '1',
		'value': '@@token@@',
		'replacement': 'ipv4'
	},
	'end': 124,
	'value': '@@host_ip@@'
}
`
a sample token with fixed value there is no need to replace
`
{
	'start': 105,
	'end': 113,
	'value': '/137 to '
}
`
