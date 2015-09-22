

import os

for filename in os.listdir("."):
  if filename.endswith(".jpg"):
    rename = filename.replace(".", "-")
    rename = rename.replace("-jpg", ".jpg")
    #print rename
    os.rename(filename, rename)
