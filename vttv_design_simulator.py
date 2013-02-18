from pylab import *

# what's presented to respondents
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

def design_matrix_convertor(original_matirx):
   pass
    
       
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
            n_attribute = (len(row) + 1) / 2
            z1 = row[0 : n_attribute]
            z2 = row[n_attribute : ] 
            p1 = self.get_logit_prob(z1,z2)
            p2 = 1 - p1
            info_matrix += outer(z1 - z2, z1 - z2) * p1 * p2
        avc=inv(info_matrix) / self.n
        derror = det(inv(info_matrix)) ** (1. / n_attribute)
        return {"avc":avc,"derror":derror}
        
if __name__ == "__main__":
    beta = array([1,0.1,0.8,1.2])
    dm = normal(size = (10,8))
    s = Simulator(beta, 10, dm)
    e_info = s.get_efficiency_info()
    print e_info["avc"]
    t_ratio = beta / e_info["avc"].diagonal()
    print t_ratio
    print e_info["derror"]
