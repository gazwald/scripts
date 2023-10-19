# Find Path

Script to traverse a Python object such as a dict or list using a period separated string, e.g.;

```python
# String path
path = "logStreams.*.logStreamName"
# Object
data = {
    'logStreams': [
        {
            'logStreamName': 'string',
            'creationTime': 123,
            'firstEventTimestamp': 123,
            'lastEventTimestamp': 123,
            'lastIngestionTime': 123,
            'uploadSequenceToken': 'string',
            'arn': 'string',
            'storedBytes': 123
        },
    ],
    'nextToken': 'string'
}

get_value(path, data)
```

Given the above scenario we'd get `"string"` in return.

## Dependencies

No external dependencies
