#!/usr/bin/env python

import numpy as np
from collections import Counter
import re

words = re.findall(r'\w+', open('die_glocke.txt').read().lower())
most_common_words = Counter(words).most_common(20)
for i in most_common_words:
  print i
