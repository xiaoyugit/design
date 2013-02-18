from random import random,randint,uniform
try:
   from pylab import *
except:
   print "this simulator requires pylab to be installed"
   
class Design:
    def __init__(self,rt,rc,bid_rand_strategy=[1,20,40,60,80],time_rand_strategy=[0.1,0.3]):
        '''reference time, reference cost, stratrified rv generating strategy'''
        self.rt=rt
        self.rc=rc
        self.bid=self.generate_bid(bid_rand_strategy)
        self.attr=self.generate_delta(time_rand_strategy)
    def generate_bid(self,strategy):
        '''unified increment for four strata'''
        increment=random()
        res=[]
        for i in range(len(strategy)-1):
            ib=(strategy[i]+int((strategy[i+1]-strategy[i])*increment))
            uwb=int((ib+strategy[-1])/2)
            dwb=int((ib+strategy[0])/2)
            res.append([ib,uwb,dwb])
        return res
    def generate_delta(self,strategy):
        '''return a dictionary of time (4*1) and cost (4*3) change'''
        delta=strategy[1]-strategy[0]
        delta_time=[max(1,int(self.rt*random()*delta)) for i in range(4)]
        delta_cost=[]
        for i,dt in enumerate(delta_time):
            ith_round_cost=map(lambda x: x*dt,self.bid[i])
            delta_cost.append(ith_round_cost)
        return {'delta_time':delta_time,'delta_cost':delta_cost}
        
    def get_attr(self):
        '''print out the attributes used in survey'''
        survey=[]
        for i in range(len(self.bid)):
            tmpOut=[]
            tmpOut.append(i+1)
            if i==0 or i==1:
                tmpOut.append('WTP')
            else:
                tmpOut.append('WTA')
            tmpOut+=[self.rt,self.rc] #not randomize the reference time and cost
            for j in range(3):
                if i==0 or i==1: #case of WTP
                    t=self.rt-self.attr['delta_time'][i]
                    c=self.rc+self.attr['delta_cost'][i][j]
                    real_bid=self.bid[i][j]
                else: #case of WTA
                    t=self.rt+self.attr['delta_time'][i]
                    c=max(10,self.rc-self.attr['delta_cost'][i][j])#constrain lowest c to be 10
                    real_bid=min(int(float(self.rc-c)/self.attr['delta_time'][i]),self.bid[i][j])
                tmpOut.append(t)
                tmpOut.append(c)
                tmpOut.append(real_bid)                     
            #print '\t'.join(map(str,tmpOut))
            survey.append(tmpOut)
        #'round type t0 c0 t1 c1 bid1 t2 c2 bid2 t3 c3 bid3'
        return survey
    def get_real_bid(self):
        '''get real vtt bid because we do not allow negative cost in WTA case'''
        return [[s[6],s[9],s[12]] for s in self.get_attr()]
 
class Person:
    def __init__(self,pid,rt,rc,vtt):
        '''initiate individual with reference cost,time and vtt'''
        self.pid=pid
        self.rt=rt
        self.rc=rc
        self.vtt=vtt
    def get_attr(self):
        print '\t'.join(map(str,[self.rt,self.rc,self.vtt]))
    def get_observation(self,design):
        '''feed individual with Design object'''
        observation=[]
        for i,bids in enumerate(design.get_real_bid()):
            ib,uwb,dwb=bids
            attr_i=design.get_attr()[i]
            t0,c0,t1,c1=attr_i[2:6]
            t2,c2=attr_i[7:9]
            t3,c3=attr_i[10:12]
            if self.vtt > ib:
                observation.append([self.pid,2*i+1,t0,c0,t1,c1,ib,0])
                if self.vtt > uwb:
                    observation.append([self.pid,2*i+2,t0,c0,t2,c2,uwb,0])
                else:
                    observation.append([self.pid,2*i+2,t0,c0,t2,c2,uwb,1])
            else:
                observation.append([self.pid,2*i+1,t0,c0,t1,c1,ib,1])
                if self.vtt > dwb:
                    observation.append([self.pid,2*i+2,t0,c0,t3,c3,dwb,0])
                else:
                    observation.append([self.pid,2*i+2,t0,c0,t3,c3,dwb,1])
        return observation
        
        
def check_bid_hist(output):
    '''check the histogram of bids in simulated dataset,depends on package "pylab"'''
    sample_bids=[obs[-2] for obs in output]
    subplot(211)
    hist(sample_bids,bins=20)
    subplot(212)
    hist(log(sample_bids),bins=20)
    show()

def check_constrained_rate(output):
    n=0
    for obs in output:
        t0,c0,t1,c1,bid=obs[2:7]
        if int(abs((c1-c0)/(t1-t0)))!=bid:
            n+=1
    print str(n)+' out of ' + str(len(output)) + ' observations are constrained'
        
if __name__=="__main__":
##input: sample size, range of reference time, cost and vtt for specifying the agents
##output: a data.frame that contains presented attributes and individual's choice
    ##parameter setting
    sample_size=int(raw_input("please type in the sample size you want to simulate:\n"))
    rt_range=[40,100]
    rc_range=[200,800]
    vtt_range=[10,40]
    sample=[Person(i,randint(rt_range[0],rt_range[1]),randint(rc_range[0],rc_range[1]),randint(vtt_range[0],vtt_range[1])) for i in range(1,sample_size+1)] 
                  
    designs=[Design(respondent.rt,respondent.rc) for respondent in sample]
    output=[]
    print 60*'-'
    for i,design in enumerate(designs):
        output+=sample[i].get_observation(design)[:]
    print '\t'.join(['pid','qid','t_A','c_A','t_B','c_B','bid','y'])
    for observation in output:
        #put output
        print '\t'.join(map(str,observation))
    
    print 60*'-'
    check_constrained_rate(output)
    check_bid_hist(output)
        

    
    
