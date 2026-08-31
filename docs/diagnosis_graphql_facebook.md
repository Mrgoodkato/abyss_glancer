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
{
    "node": {
        "body": {
            "text": "HEREISTHETEXT"
        },
        "author": {
            "_typename": "MAYBETYPEOFUSER",
            "id": "SOMESORTOFID",
            "name": "USERNAME",


        },
        "created_time": "TIMEOFCREATION"
    }
}
```
From here we can work on extracting the necessary info for each comment + user + time combo and then have a quite substantial dataset to feed to the model for verification of AI generated content.

There are also other response types that are the ones that are received once a user goes into a comment section on a post and scroll to get new comments on that post:

```yml
header: x-fb-friendly-name
header_value: CommentsListComponentsPaginationQuery

```
These use the same logic as the previous, they however don't need an enormous parsing as the comment data is easy to find in the node result.
And as a plus they come in JSON format, can be extracted using the simple `response.json()` method, easy to save and traverse without messy line by line str parsing.