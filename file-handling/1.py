with open('./test.md') as f:
    print(f.read())

import os
os.remove("ChangedFile.csv")
print("File Removed!")
