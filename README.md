# TRMNL-BinDay

A plugin for the TRMNL e-ink display.

## Configuration

### AWS Lambda
This is the backend code that calculates the bins collections that are due on the next collection day.

Create an API Gateway trigger and this provides the URL for the API.

Returns a JSON object:

```
{
  "data": {
    "date": "2025-07-15",
    "bins_due": { "blue": true, "brown": true, "green": false, "grey": false }
  }
}
```

TRMNL requires the object to hold the returned values in a "data" field.

- Create a new AWS Lambda Python function.
- Copy the function code in the function Code window.
- Deploy the function.

### TRMNL plugin
Strategy: Polling
Polling URL: https://cv0sx8t5r5.execute-api.us-east-1.amazonaws.com/default/BinCollectionPlugin
Polling verb: GET
Polling headers: Accept=application/json
