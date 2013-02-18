#########################################################################
# Pseudo code for vttv survey
#
##########################################################################

# input: departure time, reference time and reference cost [e.g. 8:00am, 9:00 am, 40 minutes and 150 JPY]
#        orthogonal design table in given format e.g.
#       mt    dt    cv    cost    mt    dt    cv    cost
#       -0.3    10    0.05    -50    -0.05    0    0.1    100
#       -0.3    0    0.1    100    -0.05    -5    0.2    150
#       -0.3    -5    0.2    150    -0.05    10    0.05    -50
#       -0.05    10    0.1    150    0.2    0    0.2    -50
#       -0.05    0    0.2    -50    0.2    -5    0.05    100
#       -0.05    -5    0.05    100    0.2    10    0.1    150
#       0.2    10    0.2    100    -0.3    0    0.05    150
#       0.2    0    0.05    150    -0.3    -5    0.1    -50
#       0.2    -5    0.1    -50    -0.3    10    0.2    100

# output: a series of choice screen being presented to respondents
#       Alternative A                            Alternative B                        
#       mt    cost    t1    t2    t3    t4    t5    mt    cost    t1    t2    t3    t4    t5
#       28    150    -4    -3    -2    -1    0    38    0    -6    -4    -2    0    2
#       28    300    -16    -14    -12    -10    -8    38    -5    -15    -11    -7    -3    1
#       28    350    -25    -21    -17    -13    -9    38    10    6    7    8    9    10
#       38    350    4    6    8    10    12    48    0    0    4    8    12    16
#       38    150    -10    -6    -2    2    6    48    -5    1    2    3    4    5
#       38    300    -9    -8    -7    -6    -5    48    10    14    16    18    20    22
#       48    300    10    14    18    22    26    28    0    -14    -13    -12    -11    -10
#       48    350    6    7    8    9    10    28    -5    -21    -19    -17    -15    -13
#       48    150    -1    1    3    5    7    28    10    -10    -6    -2    2    6

rt=raw_input("What's the travel time in your last trip")
rc=raw_input("What's the travel cost in your last trip")
dt=raw_input("What's the departure in your last trip")

def show_choice():
   '''put all the attributes on the screen'''
   #just some php form code
   pass

#transform the design attributes and show them to respondent
for term in design:
   mt1=int(rt*(1+term["mt1"]))
   mt2=int(rt*(1+term["mt2"]))
   dt1=term["dt1"]
   dt2=term["dt2"]
   std1=int(mt1*term["cv1"])
   std2=int(mt2*term["cv2"])
   cost1=int(cost+term["cost1"])
   cost2=int(cost+term["cost2"])
   t1=sample(range(mt1+dt1-std1-rt),2)+[rt]+sample(range(mt1+dt1+std1-rt),2)
   t2=sample(range(mt2+dt2-std2-rt),2)+[rt]+sample(range(mt2+dt2+std2-rt),2)
   show_case(mt1,cost1,t1[:],mt2,cost2,t2[:])
   
