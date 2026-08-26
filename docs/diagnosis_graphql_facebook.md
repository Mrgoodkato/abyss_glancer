## Diagnosis of FB graphql responses from fetcher

FB responses that include comments from users on a thread, which is the main datapoint we want to extract are detailed by a specific request header:
```yml
header: x-fb-friendly-name
header_value: CometSinglePostDialogContentQuery
```
Responses with this type of header are the ones we target with the fetcher.

When receiving the response. The information we need is under the `response.text()`, it needs to be extracted as it is a stacked JSON object string.
It's an extremely big JSON file after parsing, but we can find individual comments by checking the following keys under the nested JSON extracted file:

```JSON
"body": {
    "text": ...content
},
"author": {
    "id": ...
    "name": ...
    #Other fields may be useful in this part of the object
},
"created_time": some time value
```
From here we can work on extracting the necessary info for each comment + user + time combo and then have a quite substantial dataset to feed to the model for verification of AI generated content.