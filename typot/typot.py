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
    return {"get_event": "xxxx"}
