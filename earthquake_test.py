import os
envvar = int(os.getenv("MY_SECRET_ENV"))
newnum = envvar + 5
print("TEST RUN: " + newnum)