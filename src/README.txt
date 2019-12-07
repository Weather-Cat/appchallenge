Included in /src is app.py, db.py, and secrets.py. secrets.py hold the API key
for the weather API, it will eventually become a *.env file when run on Docker,
but I wasn't sure how to run that on something that wasn't a container.

Most of app.py and db.py is commented out. These are routes/tables that are still
in progress and/or very buggy. The uncommented routes work fine though.
Specifications for the post body for the POST route is in app.py.

UPDATE for second submission: Exactly the same as submission 1, but uncommented
POST /api/weather/ route since I was able to work out the bugs.
