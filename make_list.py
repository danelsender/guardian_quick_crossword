with open ('the_list.txt',encoding='latin-1') as f_in:
    completed = f_in.readlines()

with open ('numbers_with_type.txt','w') as f_out:
    for i,line in enumerate(completed):
        if "crossword" in line:
            useful_stuff = line.split()[0]
            num_type = useful_stuff.split("/")
            if (len(num_type) == 3):
                f_out.write (num_type[2]+"  "+num_type[1]+"\n")
