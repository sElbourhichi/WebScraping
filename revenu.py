

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 13:42:09 2020

@author: el-bourhichi
"""
import pandas as pd

data= "www.mubawab.ma_output.json.csv"
# remove unit 
def convert(s):
    d=""
    for i in range(0,len(s)):
        if s[i].isdigit():
            d=d+s[i]
    return d

   
# load data
df = pd.read_csv(data)



data=df.values
price =data[:,1]

tel=data[:,9]

jsonFile='fichierRevenu.json'
with open(jsonFile, 'w',encoding='UTF-8') as ff:
    ff.write('[')


# calculate income 
con=0
for i in range(0,len(tel)):
    
    if len(tel[i]) < 9:
        continue
    s= tel[i].split(",")
    if len(s) ==1:
        s = tel[i]
    
        
        reve=float(convert(price[i]))
        for j in range(i+1,len(tel)):
            if len( tel[j]) < 9:
                continue
            s1 = tel[j].split(",")
            if len(s1) == 1:
                s1= tel[j]
       
                if s == s1 :
                    reve1=float(convert(price[j]))
                    reve += reve1
                    price[i]=str(reve)+"DH"
                    tel[j]="[]"
               
                   # con+=1  
                    
                   
            else :
                if s1[0]+"]" == s or "["+s1[1][1:] == s :
                    
                    reve1=float(convert(price[j]))
                    reve += reve1
                    price[i]=str(reve)+"DH"
                    if s1[0]+"]" == s:
                        tel[j]=tel[j][17:]
                    else:
                        tel[j]=tel[j][:18]
               
                    #con+=1 
        
    else:            
        sa = s[0]+"]"
        sb="["+s[1][1:]
        reve=float(convert(price[i]))
        for j in range(i+1,len(tel),1):
            if len( tel[j]) < 9:
                continue
            s1=tel[j].split(",")
            if len(s1) == 1:
                s1= tel[j]
                if sa == s1 or sb== s1:
                    reve1=float(convert(price[j]))
                    reve += reve1
                    price[i]=str(reve)+"DH"
                   
                    tel[j]="[]"
                
                    #con+=1 
                    
                    
                    
            else :
                saa = s1[0]+"]"
                sbb ="["+s1[1][1:]
                if sa == saa or sa == sbb or sb==saa or sb == sbb:
                    reve1=float(convert(price[j]))
                    reve += reve1
                    price[i]=str(reve)+"DH"
                    
                    if saa == sa or saa ==sb:
                        tel[j]=tel[j][17:]
                    elif sbb == sa or sbb == sb:
                        tel[j]=tel[j][:18]
                    
                    if (saa == sa or saa ==sb) and (sbb == sa or sbb == sb):
                        tel[j]="[]"
                
                    #con+=1 
      
    if con >0 :
        with open(jsonFile, 'a',encoding='UTF-8') as ff:
            ff.write(',')   
    #preparing the json object representing one article               
    data = "{\"price\":"+"\""+str(price[i])+"\""
    data+=",\"tel\":"+"\""+str(tel[i])+"\""
    data+="}"

    with open(jsonFile, 'a',encoding='UTF-8') as ff:
        ff.write(data)
    con+=1   
#Close the json file
with open(jsonFile, 'a',encoding='UTF-8') as ff:
    ff.write(']')

df = pd.read_json(jsonFile)

#convert the json to csv 
df.to_csv(jsonFile+'.csv',sep=',', index = None, header=True, encoding="UTF-8")

                



    