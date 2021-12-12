import csv
import urllib
from sklearn.svm import SVC
import numpy as np

common_terms=["directory","faculty","faculty-staff","faculty-directory","people","people-page","staff",
              "teaching-faculty","about-people","members","all-faculty-staff","faculty-and-staff",
              "faculty-list","professors","faculty-profiles"]

class supportVectorMachineModel:
    def __init__(instance):
        instance.array_list=[]
        instance.filled=None
        instance.input_data="./train.csv"

    def start(instance):
        parts=[instance.get_all_parts(input_link) for input_link in [first[0] for first in (instance.get_all_lines(instance.input_data))]]

        for part in parts:
            for element in part:
                if element not in instance.array_list:
                    instance.array_list.append(element)
                    
        size_f=len(parts)
        size_s=len(instance.array_list)
        
        array=np.zeros([size_f, size_s],dtype=np.int)
        for current, num in enumerate(parts):
            size_t=len(instance.array_list)
            array_temp=np.zeros(size_t,dtype=np.int)
            for element in num:
                if element in instance.array_list:
                    array_temp[instance.array_list.index(element)]+=1
            
            array[current]=array_temp
        
        instance.filled=SVC(kernel="linear").fit(array,[first[1] for first in (instance.get_all_lines(instance.input_data))])

    def get_all_lines(instance,input_file):
        results=[]
        with open(input_file,"r") as tmp:
            for element in csv.reader(tmp):
                results.append(element)
        return results
        
    def analyze(instance,input_link):
        if (instance.filled is None):
            instance.start()
        
        size_f=len(instance.array_list)
        size_s=len(instance.array_list)
        array=np.zeros([1, size_f],dtype=np.int)
        array_temp=np.zeros(size_s,dtype=np.int)
        tmp_lst = [var for var in input_link.split("/") if var]
                    
        for curr in tmp_lst:
            for term in common_terms:
                if term in curr:
                    if len(curr)!=len(term):
                        tmp_lst.append(term)
        
        for element in tmp_lst:
            if element in instance.array_list:
                array_temp[instance.array_list.index(element)]+=1
    
        array[0]=array_temp
        return instance.filled.predict(array)[0]
    
    def get_all_parts(instance,input_link):
        tmp_lst=[var for var in input_link.split("/") if var]
                    
        for curr in tmp_lst:
            for term in common_terms:
                if term in curr:
                    if len(curr)!=len(term):
                        tmp_lst.append(term)

        return tmp_lst

if __name__=="__main__":
    results=[]
    classification=supportVectorMachineModel()
    classification.train()
    test_data=[first[0] for first in model.read_file("./test.csv")]