import hug


version = 1


@hug.get("/typot/get_authorized", versions=version)
@hug.local()
def get_authorized():
    pass


@hug.post("/typot", versions=version)
@hug.local()
def typot(body=None):
    print("comming!!")
    print(body)

    if "pull_request_created":
        # read pull request
        # check typo
        # make review comment
        pass
    elif "pull_request_review_comment_created":
        if "comment means adoption of typo fix":
            # get previous comment from list of review comments
            # if comment is got, adopt it
            pass

    return {"get_event": "xxxx"}
