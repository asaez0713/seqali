from nw_test import nw

f = open('test.txt','r')

Alst = []
Blst = []
words = []

lst = f.read().split('\n')[:-1]

for item in lst:
    if item == '':
        pass
    elif item[0] == 'p':
        words.append(item[7:-2])
    elif item[0] == 'A':
        Alst.append(item[6:-2])
    elif item[0] == 'B':
        Blst.append(item[6:-2])

Alst1 = [lst.split("','") for lst in Alst]
Blst1 = [lst.split("','") for lst in Blst]

f1 = open('nw_out.txt','w')
for i in range(len(Alst1)):
    f1.write(words[i]+':')
    f1.write('\n')
    f1.write(str(nw(Alst1[i],Blst1[i])[0]))
    f1.write('\n')
    f1.write(str(nw(Alst1[i],Blst1[i])[1]))
    f1.write('\n')
    f1.write('\n')