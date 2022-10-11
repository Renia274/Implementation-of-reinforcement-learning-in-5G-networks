
import shutil
import os

#list for BWPs of gNB1
result1=[]
result2=[]
result3=[]
result4=[]

def collector():
    #read the SINR tracing file and append SINR of BWPs to a list
    file = input("Please type in the full path of the folder containing your files:    ")
    f=open(file,"r")
    lines=f.readlines()

    for x in lines:

        if 'BWPID:0' in x:
            result1.append(x.split()[6:9:2])

        if 'BWPID:1' in x:
            result2.append(x.split()[6:9:2])

        if 'BWPID:2' in x:
            result3.append(x.split()[6:9:2])

        if 'BWPID:3' in x:
            result4.append(x.split()[6:9:2])

    f.close()

    # open file in write mode for BWP0
    with open(r'/home/lenovo/custom_enviroment/custom_enviroment/envs/BWPID000.txt', 'w') as fp1:
        for item in result1:
            # write each item for BWP0 on a new line
            fp1.write("%s\n" % item)
        print('Done1')

    fp1.close()

    # open file in write mode for BWP1
    with open(r'/home/lenovo/custom_enviroment/custom_enviroment/envs/BWPID111.txt', 'w') as fp2:
        for item in result2:
            # write each item for BWP1 on a new line
            fp2.write("%s\n" % item)
        print('Done2')

    fp2.close()

    # open file in write mode for BWP2
    with open(r'/home/lenovo/custom_enviroment/custom_enviroment/envs/BWPID222.txt', 'w') as fp3:
        for item in result3:
            # write each item for BWP2 on a new line
            fp3.write("%s\n" % item)
        print('Done3')

    fp3.close()

    # open file in write mode for BWP3
    with open(r'/home/lenovo/custom_enviroment/custom_enviroment/envs/BWPID333.txt', 'w') as fp4:
        for item in result4:
            # write each item for BWP3 on a new line
            fp4.write("%s\n" % item)
        print('Done4')

    fp4.close()
