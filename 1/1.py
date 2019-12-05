fuelreq = 0 
with open('input', 'r') as f:
    for l in f:
        fuelreq += int(int(l)/3.0)-2
        
print(fuelreq)
