from pylab import *
from decimal import Decimal

class Design:
    """attribute level in design matrix out"""
    def __init__(self,attr_level,orthogonal_array):
        self.attr_level = attr_level
        self.orthogonal_array = orthogonal_array
    
    def get_design_matrix(self):
        res = []
        for row in self.orthogonal_array:
            tmp = []
            for i, v in enumerate(row):
                tmp.append(self.attr_level[i%4][v-1])
            res.append(tmp)
        return res
    def get_individual_design_matrix(self,rt,rc):
        res = []
        for row in self.get_design_matrix():
            tmp = []
            for i in range(2):
                d_mt, d_dt, d_cv, d_cost = row [4 * i: 4 * i + 4]
                mt = rt * (1 + d_mt)
                cost = rc + d_cost
                std = rt * d_cv
                #rand_sd = sorted([mt + d_dt - rt - std * uniform() for i in range(2)] + [mt + d_dt - rt] + [mt + d_dt - rt + std * uniform() for i in range(2)])
                t = mt + d_dt - rt
                rand_sd = [t - std] + [t - std * 0.5] + [t] + [t + std * 0.5] + [t + std]
                tmp.extend([mt] + [cost] + rand_sd)
                tmp = map(int,tmp)
            res.append(tmp)
        return res
        
    

def design_matrix_convertor(original_matirx):
    transformed = []
    for row in original_matirx:
        sde_a = abs(sum([min(0,item) for item in row[2:7]])) * 0.2
        sde_b = abs(sum([min(0,item) for item in row[9:]])) * 0.2
        sdl_a = sum([max(0,item) for item in row[2:7]]) * 0.2
        sdl_b = sum([max(0,item) for item in row[9:]]) * 0.2
        tmp = row[:2] + [sde_a] + [sdl_a] + row[7:9] + [sde_b] + [sdl_b]
        transformed.append(tmp)
    return transformed
    
       
class Simulator:
    """beta and design in d-error out"""
    def __init__(self, beta, n, design_matrix):
        self.beta = beta
        self.design_matrix = design_matrix
        self.n = n
        
    def get_logit_prob(self,z1,z2):
        delta_u = dot(self.beta,(z2 - z1))
        p = 1 / (1 + exp(delta_u))
        return p
        
    def get_efficiency_info(self):
        info_matrix = zeros((4,4))
        for row in self.design_matrix:
            n_attribute = len(row) / 2
            z1 = row[0 : n_attribute]
            z2 = row[n_attribute : ] 
            p1 = self.get_logit_prob(z1,z2)
            p2 = 1 - p1
            info_matrix += outer(z1 - z2, z1 - z2) * p1 * p2
        avc=inv(info_matrix) / self.n
        derror = det(inv(info_matrix)) ** (1. / n_attribute)
        return {"avc":avc,"derror":derror}
        
if __name__ == "__main__":
    attr_level = genfromtxt("attribute_level.conf").T.tolist()
    o_a = genfromtxt("orthogonal_array.conf", int).tolist()
    design = Design(attr_level, o_a)
    om = design.get_individual_design_matrix(40,200)
    print "Choice sernario presented to respondent:"
    print array(om)
    dm = array(design_matrix_convertor(om))
    print "Attributes used in estimating scheduling model:"
    print array(dm,dtype=Decimal)
    beta = array([1,0.05,0.8,2.0])
    s = Simulator(beta, 300, dm)
    e_info = s.get_efficiency_info()
    #print e_info["avc"]
    print "Simulated t-ratios"
    t_ratio = beta / e_info["avc"].diagonal()
    print t_ratio
    print "D-error:"
    print e_info["derror"]
