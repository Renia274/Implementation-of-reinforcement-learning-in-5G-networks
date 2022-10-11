from typing import Optional, Union
import numpy as np
import gym
from gym import logger, spaces
from gym.error import DependencyNotInstalled
import subprocess
from AVG import summaryStats
from sinrCollector import collector
import logging

class TestCustomEnvv(gym.Env[np.ndarray, Union[int, np.ndarray]]):



    def __init__(self, render_mode: Optional[str] = None):
        #initialization spaces and arrays
        self.observation_space = spaces.Box(np.array([24.13, -4.50, 22.60, 22.35]),high=75500,dtype=np.double)
        self.action_space = spaces.Discrete(8)
        self.TxPowerAr = np.array([10.0,10.0,10.0,10.0],dtype=np.double)
        self.SINRAr = [24.13, -4.50, 22.60, 22.35]


    def step(self, action):
        #initialization the reward array
        rewardArr = np.array([0.00,0.00,0.00,0.00],dtype=np.double)



        #actions of adding TxPower for BWPs of gNB1
        if action in range(0,4):
            if action == 0:
                print(" The current vaule  of first element of the TxPower array before adding would be: {} ".format(self.TxPowerAr[0]))
                self.TxPowerAr[0] = self.TxPowerAr[0] + 30.0
                print(" The current vaule  of first element of the TxPower array after adding would be: {} ".format(self.TxPowerAr[0]))
                if self.TxPowerAr[0] > 40.0:
                    self.TxPowerAr[0] = self.TxPowerAr[0] - 30.0
                    print(" The current vaule  of first element of the TxPower array(after check) would be: {} ".format(self.TxPowerAr[0]))
                    command = './waf --run power_test31 --TxPowerGnb1Bwp0={} --TxPowerGnb1Bwp1={} --TxPowerGnb1Bwp2={} --TxPowerGnb1Bwp3={}"'.format(str(self.TxPowerAr[0]),str(self.TxPowerAr[1]),str(self.TxPowerAr[2]),str(self.TxPowerAr[3]))
                    sub1 = subprocess.Popen(command,shell=True,cwd='./en3190006/ns-3.31',bufsize=-1,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                    while True:
                        lines1 = sub1.stdout.readline()
                        if not lines1:
                            break
                        print("test1_Check1!:", lines1.split())

                    Action1_SINRs_collector = collector()

                    SINR_BWP0 = summaryStats(0)
                    self.SINRAr[0] = round(SINR_BWP0,2)
                    print(" The current vaule  of first element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[0]))

                    SINR_BWP1 = summaryStats(1)
                    self.SINRAr[1] = float(round(SINR_BWP1,2))
                    print(" The current vaule  of second element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[1]))

                    SINR_BWP2 = summaryStats(2)
                    self.SINRAr[2] = round(SINR_BWP2,2)
                    print(" The current vaule  of third element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[2]))

                    SINR_BWP3 = summaryStats(3)
                    self.SINRAr[3] = round(SINR_BWP3,2)
                    print(" The current vaule  of fourth element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[3]))

                elif self.TxPowerAr[0] <= 40.0:
                    print(" The current vaule of second element of the TxPower array(after alternative check) would be: {}".format(self.TxPowerAr[0]))
                    command = './waf --run power_test31 --TxPowerGnb1Bwp0={} --TxPowerGnb1Bwp1={} --TxPowerGnb1Bwp2={} --TxPowerGnb1Bwp3={}"'.format(str(self.TxPowerAr[0]),str(self.TxPowerAr[1]),str(self.TxPowerAr[2]),str(self.TxPowerAr[3]))
                    sub1 = subprocess.Popen(command,shell=True,cwd='./en3190006/ns-3.31',bufsize=-1,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                    while True:
                        lines1 = sub1.stdout.readline()
                        if not lines1:
                            break
                        print("test1_Check2!:", lines1.split())

                    Action1_SINRs_collector = collector()

                    SINR_BWP0 = summaryStats(0)
                    self.SINRAr[0] = round(SINR_BWP0,2)
                    print(" The current vaule  of first element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[0]))

                    SINR_BWP1 = summaryStats(1)
                    self.SINRAr[1] = float(round(SINR_BWP1,2))
                    print(" The current vaule  of second element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[1]))

                    SINR_BWP2 = summaryStats(2)
                    self.SINRAr[2] = round(SINR_BWP2,2)
                    print(" The current vaule  of third element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[2]))

                    SINR_BWP3 = summaryStats(3)
                    self.SINRAr[3] = round(SINR_BWP3,2)
                    print(" The current vaule  of fourth element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[3]))


            elif action == 1:
                print(" The current vaule  of second element of the TxPower array before adding would be: {} ".format(self.TxPowerAr[1]))
                self.TxPowerAr[1] = self.TxPowerAr[1] + 30.0
                print(" The current vaule  of second element of the TxPower array after adding would be: {} ".format(self.TxPowerAr[1]))
                if self.TxPowerAr[1] > 40.0:
                    self.TxPowerAr[1] = self.TxPowerAr[1] - 30.0
                    print(" The current vaule  of second element of the TxPower array(after check) would be: {} ".format(self.TxPowerAr[1]))
                    command = './waf --run power_test31 --TxPowerGnb1Bwp0={} --TxPowerGnb1Bwp1={} --TxPowerGnb1Bwp2={} --TxPowerGnb1Bwp3={}"'.format(str(self.TxPowerAr[0]),str(self.TxPowerAr[1]),str(self.TxPowerAr[2]),str(self.TxPowerAr[3]))
                    sub1 = subprocess.Popen(command,shell=True,cwd='./en3190006/ns-3.31',bufsize=-1,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                    while True:
                        lines1 = sub1.stdout.readline()
                        if not lines1:
                            break
                        print("test2_Check1!:", lines1.split())

                    Action2_SINRs_collector = collector()

                    SINR_BWP0 = summaryStats(0)
                    self.SINRAr[0] = round(SINR_BWP0,2)
                    print(" The current vaule  of first element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[0]))

                    SINR_BWP1 = summaryStats(1)
                    self.SINRAr[1] = float(float(round(SINR_BWP1,2)))
                    print(" The current vaule  of second element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[1]))

                    SINR_BWP2 = summaryStats(2)
                    self.SINRAr[2] = round(SINR_BWP2,2)
                    print(" The current vaule  of third element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[2]))

                    SINR_BWP3 = summaryStats(3)
                    self.SINRAr[3] = round(SINR_BWP3,2)
                    print(" The current vaule  of fourth element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[3]))



                elif self.TxPowerAr[1] <= 40.0:
                    print(" The current vaule of second element of the TxPower array(after alternative check) would be: {}".format(self.TxPowerAr[1]))
                    command = './waf --run power_test31 --TxPowerGnb1Bwp0={} --TxPowerGnb1Bwp1={} --TxPowerGnb1Bwp2={} --TxPowerGnb1Bwp3={}"'.format(str(self.TxPowerAr[0]),str(self.TxPowerAr[1]),str(self.TxPowerAr[2]),str(self.TxPowerAr[3]))
                    sub1 = subprocess.Popen(command,shell=True,cwd='./en3190006/ns-3.31',bufsize=-1,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                    while True:
                        lines1 = sub1.stdout.readline()
                        if not lines1:
                            break
                        print("test2_Check2!:", lines1.split())

                    Action2_SINRs_collector = collector()

                    SINR_BWP0 = summaryStats(0)
                    self.SINRAr[0] = round(SINR_BWP0,2)
                    print(" The current vaule  of first element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[0]))

                    SINR_BWP1 = summaryStats(1)
                    self.SINRAr[1] = float(float(round(SINR_BWP1,2)))
                    print(" The current vaule  of second element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[1]))

                    SINR_BWP2 = summaryStats(2)
                    self.SINRAr[2] = round(SINR_BWP2,2)
                    print(" The current vaule  of third element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[2]))


                    SINR_BWP3 = summaryStats(3)
                    self.SINRAr[3] = round(SINR_BWP3,2)
                    print(" The current vaule  of fourth element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[3]))




            elif action == 2:
                print(" The current vaule  of third element of the TxPower array before adding would be: {} ".format(self.TxPowerAr[2]))
                self.TxPowerAr[2] = self.TxPowerAr[2] + 30.0
                print(" The current vaule  of third element of the TxPower array after adding would be: {} ".format(self.TxPowerAr[2]))

                if self.TxPowerAr[2] > 40.0:
                    self.TxPowerAr[2] = self.TxPowerAr[2] - 30.0
                    print(" The current vaule  of third element of the TxPower array(after check) would be: {} ".format(self.TxPowerAr[2]))
                    command = './waf --run power_test31 --TxPowerGnb1Bwp0={} --TxPowerGnb1Bwp1={} --TxPowerGnb1Bwp2={} --TxPowerGnb1Bwp3={}"'.format(str(self.TxPowerAr[0]),str(self.TxPowerAr[1]),str(self.TxPowerAr[2]),str(self.TxPowerAr[3]))
                    sub1 = subprocess.Popen(command,shell=True,cwd='./en3190006/ns-3.31',bufsize=-1,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                    while True:
                        lines1 = sub1.stdout.readline()
                        if not lines1:
                            break
                        print("test3_Check1!:", lines1.split())

                    Action3_SINRs_collector = collector()

                    SINR_BWP0 = summaryStats(0)
                    self.SINRAr[0] = round(SINR_BWP0,2)
                    print(" The current vaule  of first element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[0]))

                    SINR_BWP1 = summaryStats(1)
                    self.SINRAr[1] = float(float(round(SINR_BWP1,2)))
                    print(" The current vaule  of second element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[1]))

                    SINR_BWP2 = summaryStats(2)
                    self.SINRAr[2] = round(SINR_BWP2,2)
                    print(" The current vaule  of third element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[2]))

                    SINR_BWP3 = summaryStats(3)
                    self.SINRAr[3] = round(SINR_BWP3,2)
                    print(" The current vaule  of fourth element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[3]))



                elif self.TxPowerAr[2] <= 40.0:
                    print(" The current vaule of third element of the TxPower array(after alternative check) would be: {}".format(self.TxPowerAr[2]))
                    command = './waf --run power_test31 --TxPowerGnb1Bwp0={} --TxPowerGnb1Bwp1={} --TxPowerGnb1Bwp2={} --TxPowerGnb1Bwp3={}"'.format(str(self.TxPowerAr[0]),str(self.TxPowerAr[1]),str(self.TxPowerAr[2]),str(self.TxPowerAr[3]))
                    sub1 = subprocess.Popen(command,shell=True,cwd='./en3190006/ns-3.31',bufsize=-1,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                    while True:
                        lines1 = sub1.stdout.readline()
                        if not lines1:
                            break
                        print("test3_Check2!:", lines1.split())

                    Action3_SINRs_collector = collector()

                    SINR_BWP0 = summaryStats(0)
                    self.SINRAr[0] = round(SINR_BWP0,2)
                    print(" The current vaule  of first element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[0]))

                    SINR_BWP1 = summaryStats(1)
                    self.SINRAr[1] = round(SINR_BWP1,2)
                    print(" The current vaule  of second element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[1]))

                    SINR_BWP2 = summaryStats(2)
                    self.SINRAr[2] = round(SINR_BWP2,2)
                    print(" The current vaule  of third element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[2]))

                    SINR_BWP3 = summaryStats(3)
                    self.SINRAr[3] = round(SINR_BWP3,2)
                    print(" The current vaule  of fourth element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[3]))


            elif action == 3:
                print(" The current vaule  of fourth element of the TxPower array before adding would be: {} ".format(self.TxPowerAr[3]))
                self.TxPowerAr[3] = self.TxPowerAr[3] + 30.0
                print(" The current vaule  of fourth element of the TxPower array after adding would be: {} ".format(self.TxPowerAr[3]))
                if self.TxPowerAr[3] > 40.0:
                    self.TxPowerAr[3] = self.TxPowerAr[3] - 30.0
                    print(" The current vaule  of third element of the TxPower array(after check) would be: {} ".format(self.TxPowerAr[3]))
                    command = './waf --run power_test31 --TxPowerGnb1Bwp0={} --TxPowerGnb1Bwp1={} --TxPowerGnb1Bwp2={} --TxPowerGnb1Bwp3={}"'.format(str(self.TxPowerAr[0]),str(self.TxPowerAr[1]),str(self.TxPowerAr[2]),str(self.TxPowerAr[3]))
                    sub1 = subprocess.Popen(command,shell=True,cwd='./en3190006/ns-3.31',bufsize=-1,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                    while True:
                        lines1 = sub1.stdout.readline()
                        if not lines1:
                            break
                        print("test4_Check1!:", lines1.split())

                    Action4_SINRs_collector = collector()

                    SINR_BWP0 = summaryStats(0)
                    self.SINRAr[0] = round(SINR_BWP0,2)
                    print(" The current vaule  of first element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[0]))

                    SINR_BWP1 = summaryStats(1)
                    self.SINRAr[1] = round(SINR_BWP1,2)
                    print(" The current vaule  of second element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[1]))

                    SINR_BWP2 = summaryStats(2)
                    self.SINRAr[2] = round(SINR_BWP2,2)
                    print(" The current vaule  of third element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[2]))

                    SINR_BWP3 = summaryStats(3)
                    self.SINRAr[3] = round(SINR_BWP3,2)
                    print(" The current vaule  of fourth element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[3]))



                elif self.TxPowerAr[3] <= 40.0:
                    print(" The current vaule of fourth element of the TxPower array(after alternative check) would be: {}".format(self.TxPowerAr[3]))
                    command = './waf --run power_test31 --TxPowerGnb1Bwp0={} --TxPowerGnb1Bwp1={} --TxPowerGnb1Bwp2={} --TxPowerGnb1Bwp3={}"'.format(str(self.TxPowerAr[0]),str(self.TxPowerAr[1]),str(self.TxPowerAr[2]),str(self.TxPowerAr[3]))
                    sub1 = subprocess.Popen(command,shell=True,cwd='./en3190006/ns-3.31',bufsize=-1,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                    while True:
                        lines1 = sub1.stdout.readline()
                        if not lines1:
                            break
                        print("test4_Check2!:", lines1.split())

                    Action4_SINRs_collector = collector()

                    SINR_BWP0 = summaryStats(0)
                    self.SINRAr[0] = round(SINR_BWP0,2)
                    print(" The current vaule  of first element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[0]))

                    SINR_BWP1 = summaryStats(1)
                    self.SINRAr[1] = round(SINR_BWP1,2)
                    print(" The current vaule  of second element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[1]))

                    SINR_BWP2 = summaryStats(2)
                    self.SINRAr[2] = round(SINR_BWP2,2)
                    print(" The current vaule  of third element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[2]))

                    SINR_BWP3 = summaryStats(3)
                    self.SINRAr[3] = round(SINR_BWP3,2)
                    print(" The current vaule  of fourth element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[3]))


        #actions of substracting TxPower for BWPs of gNB1
        elif action in range(4,8):
            if action == 4:
                print(" The current vaule  of first element of the TxPower array before substraction would be: {} ".format(self.TxPowerAr[0]))
                self.TxPowerAr[0] = self.TxPowerAr[0] - 30.0
                print(" The current vaule  of first element of the TxPower array after substraction would be: {} ".format(self.TxPowerAr[0]))
                if self.TxPowerAr[0] < 10.0:
                    self.TxPowerAr[0] = self.TxPowerAr[0] + 30.0
                    print(" The current vaule  of first element of the TxPower array(after check) would be: {} ".format(self.TxPowerAr[0]))
                    command = './waf --run power_test31 --TxPowerGnb1Bwp0={} --TxPowerGnb1Bwp1={} --TxPowerGnb1Bwp2={} --TxPowerGnb1Bwp3={}"'.format(str(self.TxPowerAr[0]),str(self.TxPowerAr[1]),str(self.TxPowerAr[2]),str(self.TxPowerAr[3]))
                    sub1 = subprocess.Popen(command,shell=True,cwd='./en3190006/ns-3.31',bufsize=-1,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                    while True:
                        lines1 = sub1.stdout.readline()
                        if not lines1:
                            break
                        print("test5_Check1!:", lines1.split())

                    Action5_SINRs_collector = collector()

                    SINR_BWP0 = summaryStats(0)
                    self.SINRAr[0] = round(SINR_BWP0,2)
                    print(" The current vaule  of first element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[0]))

                    SINR_BWP1 = summaryStats(1)
                    self.SINRAr[1] = float(float(round(SINR_BWP1,2)))
                    print(" The current vaule  of second element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[1]))

                    SINR_BWP2 = summaryStats(2)
                    self.SINRAr[2] = round(SINR_BWP2,2)
                    print(" The current vaule  of third element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[2]))

                    SINR_BWP3 = summaryStats(3)
                    self.SINRAr[3] = round(SINR_BWP3,2)
                    print(" The current vaule  of fourth element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[3]))


                elif self.TxPowerAr[0] >= 10.0:
                    print(" The current vaule of second element of the TxPower array(after alternative check) would be: {}".format(self.TxPowerAr[0]))
                    command = './waf --run power_test31 --TxPowerGnb1Bwp0={} --TxPowerGnb1Bwp1={} --TxPowerGnb1Bwp2={} --TxPowerGnb1Bwp3={}"'.format(str(self.TxPowerAr[0]),str(self.TxPowerAr[1]),str(self.TxPowerAr[2]),str(self.TxPowerAr[3]))
                    sub1 = subprocess.Popen(command,shell=True,cwd='./en3190006/ns-3.31',bufsize=-1,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                    while True:
                        lines1 = sub1.stdout.readline()
                        if not lines1:
                            break
                        print("test5_Check2!:", lines1.split())

                    Action5_SINRs_collector = collector()

                    SINR_BWP0 = summaryStats(0)
                    self.SINRAr[0] = round(SINR_BWP0,2)
                    print(" The current vaule  of first element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[0]))

                    SINR_BWP1 = summaryStats(1)
                    self.SINRAr[1] = float(float(round(SINR_BWP1,2)))
                    print(" The current vaule  of second element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[1]))

                    SINR_BWP2 = summaryStats(2)
                    self.SINRAr[2] = round(SINR_BWP2,2)
                    print(" The current vaule  of third element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[2]))

                    SINR_BWP3 = summaryStats(3)
                    self.SINRAr[3] = round(SINR_BWP3,2)
                    print(" The current vaule  of fourth element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[3]))

            elif action == 5:
                print(" The current vaule  of second element of the TxPower array before substraction would be: {} ".format(self.TxPowerAr[1]))
                self.TxPowerAr[1] = self.TxPowerAr[1] - 30.0
                print(" The current vaule  of second element of the TxPower array after substraction would be: {} ".format(self.TxPowerAr[1]))

                if self.TxPowerAr[1] < 10.0:
                    self.TxPowerAr[1] = self.TxPowerAr[1] + 30.0
                    print(" The current vaule  of second element of the TxPower array(after check) would be: {} ".format(self.TxPowerAr[1]))
                    command = './waf --run power_test31 --TxPowerGnb1Bwp0={} --TxPowerGnb1Bwp1={} --TxPowerGnb1Bwp2={} --TxPowerGnb1Bwp3={}"'.format(str(self.TxPowerAr[0]),str(self.TxPowerAr[1]),str(self.TxPowerAr[2]),str(self.TxPowerAr[3]))
                    sub1 = subprocess.Popen(command,shell=True,cwd='./en3190006/ns-3.31',bufsize=-1,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                    while True:
                        lines1 = sub1.stdout.readline()
                        if not lines1:
                            break
                        print("test6_Check1!:", lines1.split())

                    Action6_SINRs_collector = collector()

                    SINR_BWP0 = summaryStats(0)
                    self.SINRAr[0] = round(SINR_BWP0,2)
                    print(" The current vaule  of first element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[0]))

                    SINR_BWP1 = summaryStats(1)
                    self.SINRAr[1] = round(SINR_BWP1,2)
                    print(" The current vaule  of second element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[1]))

                    SINR_BWP2 = summaryStats(2)
                    self.SINRAr[2] = round(SINR_BWP2,2)
                    print(" The current vaule  of third element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[2]))

                    SINR_BWP3 = summaryStats(3)
                    self.SINRAr[3] = round(SINR_BWP3,2)
                    print(" The current vaule  of fourth element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[3]))



                elif self.TxPowerAr[1] >= 10.0:
                    print(" The current vaule of second element of the TxPower array(after alternative check) would be: {}".format(self.TxPowerAr[1]))
                    command = './waf --run "power_test31 --TxPowerGnb1Bwp0={} --TxPowerGnb1Bwp1={} --TxPowerGnb1Bwp2={} --TxPowerGnb1Bwp3={}"'.format(str(self.TxPowerAr[0]),str(self.TxPowerAr[1]),str(self.TxPowerAr[2]),str(self.TxPowerAr[3]))
                    sub1 = subprocess.Popen(command,shell=True,cwd='./en3190006/ns-3.31',bufsize=-1,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                    while True:
                        lines1 = sub1.stdout.readline()
                        if not lines1:
                            break
                        print("test6_Check2!:", lines1.split())

                    Action6_SINRs_collector = collector()

                    SINR_BWP0 = summaryStats(0)
                    self.SINRAr[0] = round(SINR_BWP0,2)
                    print(" The current vaule  of first element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[0]))

                    SINR_BWP1 = summaryStats(1)
                    self.SINRAr[1] = round(SINR_BWP1,2)
                    print(" The current vaule  of second element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[1]))

                    SINR_BWP2 = summaryStats(2)
                    self.SINRAr[2] = round(SINR_BWP2,2)
                    print(" The current vaule  of third element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[2]))

                    SINR_BWP3 = summaryStats(3)
                    self.SINRAr[3] = round(SINR_BWP3,2)
                    print(" The current vaule  of fourth element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[3]))


            elif action == 6:
                print(" The current vaule  of third element of the TxPower array before substraction would be: {} ".format(self.TxPowerAr[2]))
                self.TxPowerAr[2] = self.TxPowerAr[2] - 30.0
                print(" The current vaule  of third element of the TxPower array after substraction would be: {} ".format(self.TxPowerAr[2]))

                if self.TxPowerAr[2] < 10.0:
                    self.TxPowerAr[2] = self.TxPowerAr[2] + 30.0
                    print(" The current vaule  of third element of the TxPower array(after check) would be: {} ".format(self.TxPowerAr[2]))
                    command = './waf --run power_test31 --TxPowerGnb1Bwp0={} --TxPowerGnb1Bwp1={} --TxPowerGnb1Bwp2={} --TxPowerGnb1Bwp3={}"'.format(str(self.TxPowerAr[0]),str(self.TxPowerAr[1]),str(self.TxPowerAr[2]),str(self.TxPowerAr[3]))
                    sub1 = subprocess.Popen(command,shell=True,cwd='./en3190006/ns-3.31',bufsize=-1,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                    while True:
                        lines1 = sub1.stdout.readline()
                        if not lines1:
                            break
                        print("test7_Check1!:", lines1.split())

                    Action7_SINRs_collector = collector()

                    SINR_BWP0 = summaryStats(0)
                    self.SINRAr[0] = round(SINR_BWP0,2)
                    print(" The current vaule  of first element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[0]))

                    SINR_BWP1 = summaryStats(1)
                    self.SINRAr[1] = round(SINR_BWP1,2)
                    print(" The current vaule  of second element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[1]))

                    SINR_BWP2 = summaryStats(2)
                    self.SINRAr[2] = round(SINR_BWP2,2)
                    print(" The current vaule  of third element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[2]))

                    SINR_BWP3 = summaryStats(3)
                    self.SINRAr[3] = round(SINR_BWP3,2)
                    print(" The current vaule  of fourth element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[3]))


                elif self.TxPowerAr[2] >= 10.0:
                    print(" The current vaule of third element of the TxPower array(after alternative check) would be: {}".format(self.TxPowerAr[2]))
                    command = './waf --run power_test31 --TxPowerGnb1Bwp0={} --TxPowerGnb1Bwp1={} --TxPowerGnb1Bwp2={} --TxPowerGnb1Bwp3={}"'.format(str(self.TxPowerAr[0]),str(self.TxPowerAr[1]),str(self.TxPowerAr[2]),str(self.TxPowerAr[3]))
                    sub1 = subprocess.Popen(command,shell=True,cwd='./en3190006/ns-3.31',bufsize=-1,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                    while True:
                        lines1 = sub1.stdout.readline()
                        if not lines1:
                            break
                        print("test7_Check2!:", lines1.split())

                    Action7_SINRs_collector = collector()

                    SINR_BWP0 = summaryStats(0)
                    self.SINRAr[0] = round(SINR_BWP0,2)
                    print(" The current vaule  of first element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[0]))

                    SINR_BWP1 = summaryStats(1)
                    self.SINRAr[1] = float(float(round(SINR_BWP1,2)))
                    print(" The current vaule  of second element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[1]))

                    SINR_BWP2 = summaryStats(2)
                    self.SINRAr[2] = round(SINR_BWP2,2)
                    print(" The current vaule  of third element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[2]))

                    SINR_BWP3 = summaryStats(3)
                    self.SINRAr[3] = round(SINR_BWP3,2)
                    print(" The current vaule  of fourth element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[3]))



            elif action == 7:
                print(" The current vaule  of fourth element of the TxPower array before adding would be: {} ".format(self.TxPowerAr[3]))
                self.TxPowerAr[3] = self.TxPowerAr[3] - 30.0
                print(" The current vaule  of fourth element of the TxPower array after adding would be: {} ".format(self.TxPowerAr[3]))
                if self.TxPowerAr[3] < 10.0:
                    self.TxPowerAr[3] = self.TxPowerAr[3] + 30.0
                    print(" The current vaule  of third element of the TxPower array(after check) would be: {} ".format(self.TxPowerAr[3]))
                    command = './waf --run power_test31 --TxPowerGnb1Bwp0={} --TxPowerGnb1Bwp1={} --TxPowerGnb1Bwp2={} --TxPowerGnb1Bwp3={}"'.format(str(self.TxPowerAr[0]),str(self.TxPowerAr[1]),str(self.TxPowerAr[2]),str(self.TxPowerAr[3]))
                    sub1 = subprocess.Popen(command,shell=True,cwd='./en3190006/ns-3.31',bufsize=-1,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                    while True:
                        lines1 = sub1.stdout.readline()
                        if not lines1:
                            break
                        print("test8_Check1!:", lines1.split())

                    Action8_SINRs_collector = collector()

                    SINR_BWP0 = summaryStats(0)
                    self.SINRAr[0] = round(SINR_BWP0,2)
                    print(" The current vaule  of first element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[0]))

                    SINR_BWP1 = summaryStats(1)
                    self.SINRAr[1] = round(SINR_BWP1,2)
                    print(" The current vaule  of second element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[1]))

                    SINR_BWP2 = summaryStats(2)
                    self.SINRAr[2] = round(SINR_BWP2,2)
                    print(" The current vaule  of third element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[2]))

                    SINR_BWP3 = summaryStats(3)
                    self.SINRAr[3] = round(SINR_BWP3,2)
                    print(" The current vaule  of fourth element of the SINR array(after check) would be: {:.2f}".format(self.SINRAr[3]))

                elif self.TxPowerAr[3] >= 10.0:
                    print(" The current vaule of fourth element of the TxPower array(after alternative check) would be: {}".format(self.TxPowerAr[3]))
                    command = './waf --run power_test31 --TxPowerGnb1Bwp0={} --TxPowerGnb1Bwp1={} --TxPowerGnb1Bwp2={} --TxPowerGnb1Bwp3={}"'.format(str(self.TxPowerAr[0]),str(self.TxPowerAr[1]),str(self.TxPowerAr[2]),str(self.TxPowerAr[3]))
                    sub1 = subprocess.Popen(command,shell=True,cwd='./en3190006/ns-3.31',bufsize=-1,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                    while True:
                        lines1 = sub1.stdout.readline()
                        if not lines1:
                            break
                        print("test8_Check2!:", lines1.split())

                    Action8_SINRs_collector = collector()

                    SINR_BWP0 = summaryStats(0)
                    self.SINRAr[0] = round(SINR_BWP0,2)
                    print(" The current vaule  of first element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[0]))

                    SINR_BWP1 = summaryStats(1)
                    self.SINRAr[1] = round(SINR_BWP1,2)
                    print(" The current vaule  of second element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[1]))

                    SINR_BWP2 = summaryStats(2)
                    self.SINRAr[2] = round(SINR_BWP2,2)
                    print(" The current vaule  of third element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[2]))

                    SINR_BWP3 = summaryStats(3)
                    self.SINRAr[3] = round(SINR_BWP3,2)
                    print(" The current vaule  of fourth element of the SINR array(after alternative check) would be: {:.2f}".format(self.SINRAr[3]))


        self.state = self.SINRAr

        #reward based on quality of the signal
        for i in range(len(self.SINRAr)):
            #if it is true ,then it is excellent signal
            if self.SINRAr[i] >= 20:

                print('excellent signal')
                rewardArr[0] = rewardArr[0] + 3


            #if it is true ,then it is good signal
            elif self.SINRAr[i] >= 13.00 and self.SINRAr[i] <=19.99:
                print('good signal')
                rewardArr[1] = rewardArr[1] + 2


            #if it is true ,then it is bad signal
            elif self.SINRAr[i] >= 1.00 and self.SINRAr[i] <= 12.99:
                print('bad signal')
                rewardArr[2] = rewardArr[2] -2

            #if it is true ,then it is very bad signal
            elif self.SINRAr[i] <= 0.0:
                print('very bad signal')
                rewardArr[3] = rewardArr[3] - 3
                continue



        #calculation of total reward
        total_reward = rewardArr[0] + rewardArr[1] + rewardArr[2] + rewardArr[3]

        done = False

        if total_reward>=7.0:
            done = True



        return np.array(self.state, dtype=np.double), total_reward, done, {}

    #initialization of TxPower and SINR array at the start of the episode
    def reset_array(self):

        self.array_reset1 = np.array([10.0,10.0,10.0,10.0],dtype=np.double)
        self.TxPowerAr = self.array_reset1

        self.array_reset2 = np.array([24.13, -4.50, 22.60, 22.35], dtype=np.double)
        self.SINRAr = self.array_reset2

        return self.TxPowerAr, self.SINRAr

    #initialization of the eviroment at the start of the episode
    def reset(
        self,
        *,
        seed: Optional[int] = None,
        return_info: bool = False,
        options: Optional[dict] = None,
    ):
        super().reset(seed=seed)


        self.state = self.SINRAr

        if not return_info:
            return np.array(self.state, dtype=np.double)
        else:
            return np.array(self.state, dtype=np.double), {}
