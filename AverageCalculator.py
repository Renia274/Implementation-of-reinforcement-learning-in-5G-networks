

from __future__ import division
import shutil

def summaryStats(number: int):
    #checks the input file
    if (number == 0):
        file3 = '/home/lenovo/custom_enviroment/custom_enviroment/envs/BWPID000.txt'
    elif (number == 1):
        file3 = '/home/lenovo/custom_enviroment/custom_enviroment/envs/BWPID111.txt'
    elif (number == 2):
        file3 = '/home/lenovo/custom_enviroment/custom_enviroment/envs/BWPID222.txt'
    elif (number == 3):
        file3 = '/home/lenovo/custom_enviroment/custom_enviroment/envs/BWPID333.txt'
    else:
        file3 = input("enter the test BWP file:    ")
    #open the file
    with open(file3) as f6:
        #calculation of average for SINR of every SINR and return the result
            data = [float(eval(line6)[-1]) for line6 in f6]

            average = sum(data)/len(data)

    print("The average value is ", average)
    f6.close()
    return average
