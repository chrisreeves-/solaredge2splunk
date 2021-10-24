# Send SolarEdge Power Usage to Splunk

## TL;DR
A Python script to get the power usage from the Solaredge API and send it to Splunk

## Configuration

### AWS Lambda
1. Make sure the handler equals:

<pre>
<thefilenameofthepythonfile>.main
</pre>

### Lambda Environemnt Variables
You will need to add the following environment variables to your AWS Lambda function

<pre>
solaredgeurl
solaredgesite
solaredgeapikey
splunkurl
splunkapi
</pre>

### Splunk Data Input

1. Create a "HTTP event collector"
2. Change source type to "json_no_timestamp"

Use the token created as the "splunkapi" value