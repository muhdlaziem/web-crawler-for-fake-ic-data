import random
import pandas as pd

nric = []
data = pd.read_csv("IC_data.csv")

def randomNric():
    y = (random.randint(70,99)) * 10000
    m = (random.randint(1,12)) * 100
    d = (random.randint(0,28))
    birth = y+m+d

    state = (random.randint(1,40))

    if (state < 10):
        state = "-0" + str(state)
    else:
        state = "-" + str(state)
    
    rand3 = (random.randint(100,999))
    
    ic = str(birth) + str(state) + "-" + str(rand3)
    return ic 

def backNumber():
    bck = (random.randint(0,4)) * 2
    bck = "-0" + str(bck) + "-01"
    
    return bck

nric=[]
nricBack=[]

for N in data["Sex"]:

    ic = randomNric()

    if N == "PEREMPUAN":
        even = (random.randint(0,4)) * 2
        ic = ic + str(even)
        
        bck = ic + backNumber()

        nric.append(ic)
        nricBack.append(bck)


    else:
        odd = (random.randint(0,4)) * 2 + 1
        ic = ic + str(odd)
        
        bck = ic + backNumber()

        nric.append(ic)
        nricBack.append(bck)


data["NRIC"] = nric
data["Back_NRIC"] = nricBack

data.to_csv('IC_data_with_NRIC.csv', index=False)
