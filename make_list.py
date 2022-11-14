with open ('the_list.txt',encoding='latin-1') as f_in:
    completed = f_in.readlines()

f_p = open('partial.txt','w')
f_c = open('complete.txt','w')
for line in completed:
    col0 = line.split()[0]
    if "crosswords/quick" in col0:
        num = col0.split("/")[2]
        if (line.count('""""') > 100):
            f_p.write (num+"\n")
        f_c.write (num+"\n")

