#########################################################################
# Pseudo code for adaptive design 
# 1. fixed increment in 4strataRand() to make it more like sequence draw
# 2. following question depends on previous question on each round
##########################################################################

# input: reference time and reference cost [e.g. 40 minutes and 150 JPY]
#       lower bound and upper bound of VTT-BID [e.g. 1 JPY/min - 80 JPY/min]
#       lower bound and upper bound of percentage change of TIME [e.g. 10% - 30%]


def 4strataRand(lowerBound, upperBound):  
    '''Generate 4 random numbers from 4 stratas within the given range'''
    strataInterval = ( upperBound - lowerBound ) / 4
    result = []
    increment = strataInterval * rand()
    for i = 1 to 4:
        case condition of
            #rand() is a random number generator for range of (0, 1)
            i == 1 : result.append ( lowerBound + increment )
            i == 2 : result.append ( lowerBound + strataInterval + increment )
            i == 3 : result.append ( lowerBound + strataInterval * 2 + increment )
            i == 4 : result.append ( lowerBound + strataInterval * 3 + increment )
        end case
    #randomize the sequence of elements in result, most programing language should have such a built-in function
    result.randomSeq()
    return result

def round(v):
    '''round the value to -1 digits, e.g: 111.1 -->> 110'''
    return int(v/10) * 10

def show(i,j):
    '''show 4 choice scenarios in random position'''
    if rand() >= 0.5:
        print 'ROUTE: ' + Time1[i][j] + 'minute ' + Cost1[i][j] + 'JPY /n'
        print 'ROUTE: ' + Time2[i][j] + 'minute ' + Cost2[i][j] + 'JPY /n'
        input("Which route would you like to choose?")
    else: 
        print 'ROUTE: ' + Time2[i][j] + 'minute ' + Cost2[i][j] + 'JPY /n'
        print 'ROUTE: ' + Time1[i][j] + 'minute ' + Cost1[i][j] + 'JPY /n'
        input("Which route would you like to choose?")

def main():
    '''main function'''
    drawVtt = 4strataRand( lowerBoundVtt, upperBoundVtt )
    drawTime = 4strataRand( lowerBoundTime, upperBoundTime )
    Time1[i][0] = round ( ( 0.9 + 0.2 * rand() ) * refTime1 )
    Cost1[i][0] = round ( ( 0.9 + 0.2 * rand() ) * refCost1 )
    for i = 1 to 5:
        case condition of
            i == 1 or 2:
                #WTP
                deltaT=round ( drawTime[i] * Time1[i][0] )
                deltaC=round ( drawVtt[i] * drawTime[i] * Time1[i][0] )
                deltaCDown=round ( (drawVtt[i] + upperBoundVTT)/2 * drawTime[i] * Time1[i][0] )
                deltaCUp=round ( (drawVtt[i] + lowerBoundVTT)/2 * drawTime[i] * Time1[i][0] )
                Time2[i][0] = Time1[i][0] - deltaT
                Cost2[i][0] = Cost1[i][0] + deltaC
                Time2[i][1] = Time1[i][0]
                Cost2[i][1] = Cost1[i][0] + deltaCDown
                Time2[i][2] = Time1[i][0]
                Cost2[i][2] = Cost1[i][0] + deltaCUp
            i == 3 or 4:
                #WTA
                MaxTimeDiff = Cost1[i][0] / upperBoundVtt 
                deltaT=round ( min( drawTime[i] * Time1[i][0], MaxTimeDiff ) )
                deltaC=round ( drawVtt[i] * min( drawTime[i] * Time1[i][0], MaxTimeDiff ) )
                deltaCDown=round ( (drawVtt[i] + upperBoundVTT)/2 * min( drawTime[i] * Time1[i], MaxTimeDiff ) )
                deltaCUp=round ( (drawVtt[i] + lowerBoundVTT)/2 * min( drawTime[i] * Time1[i], MaxTimeDiff ) )
                Time2[i][0] = Time1[i][0] + deltaT
                Cost2[i][0] = Cost1[i][0] - deltaC
                Time2[i][1] = Time1[i][0]
                Cost2[i][1] = Cost1[i][0] - deltaCDown
                Time2[i][2] = Time1[i][0]
                Cost2[i][2] = Cost1[i][0] - deltaCUp
            i == 5
                #Dominated
                Time2[i][0]=Time1[i][0] + 10
                Cost2[i][0]=Cost1[i][0] + 100

        end case

    Seq = [1,2,3,4]
    #randomize the sequence of 4 scenarios showing up
    Seq.randomSeq()

    for i in Seq:
        show(i,0)
        response=userInput()
        if response = "fast and expensive one":
            show(i,2)
        else:
            show(i,1)
        

    #dominant choice question showing up
    show(5,0)

if __name__='__main__':
    main()
