import time

t1 = time.time()
for i in range(1000000):
    for j in range(100):
        str(j)
t2 = time.time()
print(t2-t1)