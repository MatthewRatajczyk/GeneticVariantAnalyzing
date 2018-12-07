"""
Organizes a spreadsheet of data based on the gene and paitent to to variants

Author: Matthew Ratajczyk
"""

import pandas as pd
import numpy as np

data = pd.read_csv("~/Downloads/CNV_challenge_5.csv") #reads the file into the program
FinalData = data.drop_duplicates(subset=['orderid', 'gene','call']).reset_index(drop=True) #Drops all Duplicates, and Re-aranges index
ListOfData = list() #Creates an emply list, This will be a list of lists that we can add to our final Datafram PizzaTime
for Value in range(len(FinalData.index)): #Here we will itterate through all of the values in FinalData, and the corolating values to ListOfData 
    if FinalData.call[Value] == 'neutral':
       ListOfData.append([FinalData.orderid[Value], FinalData.gene[Value],0,1,0])
    elif FinalData.call[Value] == 'loss':
       ListOfData.append([FinalData.orderid[Value], FinalData.gene[Value],1,0,0])
    elif FinalData.call[Value] == 'gain':
       ListOfData.append([FinalData.orderid[Value], FinalData.gene[Value],0,0,1])
    #Since there are alot of neutral's its best to have that be the first if statment.   
PizzaTime = pd.DataFrame(ListOfData, columns = ['Orderid','Gene', 'Loss', 'neutral', 'gain']) #Here we add our ListOfData to the PizzaTime DataFrame
ToBreak = len(PizzaTime.index) # this stops our null pointer error, and allows for next conditonal checking
#The Pizza time dataframe will have 2 entries for loss and neutral even if they are the same orderid and gene we need to merge them and delete the duplicate
for Value in range(len(PizzaTime.index)): #
    if Value == ToBreak-1: #will stop us once we reach the end of the list so we don't try to compare the next value to something that dose not exsist.
        break
    elif PizzaTime.Orderid[Value] == PizzaTime.Orderid[Value+1]:#Here we compare the gene and order id if they match we add them together, then delete the duplicate
        if PizzaTime.Gene[Value] == PizzaTime.Gene[Value+1]:
            PizzaTime.loc[Value+1, 'Loss'] = PizzaTime.Loss[Value] + PizzaTime.Loss[Value+1]
            PizzaTime.loc[Value+1, 'neutral'] = PizzaTime.neutral[Value] + PizzaTime.neutral[Value+1]
            PizzaTime.loc[Value+1, 'gain'] = PizzaTime.gain[Value] + PizzaTime.gain[Value+1]
            print(Value)
            PizzaTime = PizzaTime.drop(Value)
            #loc vs ix as it was discontinued 
PizzaTime = PizzaTime.reset_index(drop=True) #Here we have to rest the index as its out of order from us deleting duplicate rows. Better to do this out side the for loop.
