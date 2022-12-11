import os

if os.path.exists("out"):
    for filename in os.listdir("out"):
        os.remove("out/" + filename)
    os.rmdir("out")

if os.path.exists("fonts"):
    for filename in os.listdir("fonts"):
        os.remove("fonts/" + filename)
    os.rmdir("fonts")