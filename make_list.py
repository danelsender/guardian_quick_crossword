with open ('the_list.txt',encoding='latin-1') as f_in:
    completed = f_in.readlines()

f_p = open('partial.txt','w')
f_c = open('complete.txt','w')
for i,line in enumerate(completed):
    if "crosswords/quick" in line:
        useful_stuff = line.split()[0]
        num_type = useful_stuff.split("/")
        if (len(num_type) == 3):
            if (line.count('""""') > 75):
                f_p.write (num_type[2]+"\n")
            else:
                f_c.write (num_type[2]+"\n")

