s= "1222311"
from itertools import groupby
for key , group in groupby(s):
     print((len(list(group)), int(key)), end=' ')