#!/bin/python

import sys

bam_names = ""

for file in sys.argv[1].split(","):
  if len(bam_names) > 0:
    bam_names += ","

  bam_names += file.split("/")[-1].split(".")[0]

print bam_names
