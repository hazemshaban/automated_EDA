import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, Image
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
##################################################################################################################


class EDA:
  
  ############### reading the file  ###################
  def __init__(self,dataset_Path,type='csv'):
    if type=='csv':
      self.dataset=pd.read_csv(dataset_Path)
    elif type=='xlsx':
      self.dataset=pd.read_excel(dataset_Path)
    else: 
      print('invalid type')



  ############### columns datatypes###################
  def col_dtypes(self):
    return self.dataset.dtypes


  ############### handling missing values ########################
  def handling_missing_values(self):
      print("\nnumber of null values in each column\n")
      print(self.dataset.isnull().sum())
      print('\nDrops rows with any missing values\n')
      self.dataset=self.dataset.dropna()  # Drops rows with any missing values
      print(self.dataset.isnull().sum())


  ################  remove duplicates ########################
  def remove_duplicates(self):
      print('\n############## duplicates ############\n')
      for col in self.dataset.columns.tolist():
            print('{} = {}'.format(col,self.dataset.duplicated(col).sum()))
      
      print('\nnumber of duplicated rows={}'.format(self.dataset.duplicated().sum()))
      self.dataset.drop_duplicates()
      print('After dropping:: number of duplicated rows={}'.format(self.dataset.duplicated().sum()))
 
 
  ################ scaling numerical values ##################### 
  def scaling_numerical_values(self):
    print('\n################ scaling ###############\n')
    print('\nchoose which column you need to scale')
    i=1
    dic={}
    print('{}-{}'.format(0,'back'))
    for col in  self.dataset.select_dtypes(include=['number']).columns.tolist():  
      print('{}-{}'.format(i,col))
      dic[i]=col
      i+=1
    index=int(input())
    if index==0:return
    if index not in range(len(self.dataset.select_dtypes(include=['number']).columns.tolist())+1):
      print('invalid choise')
      return
    # Create a MinMaxScaler object
    scaler = MinMaxScaler() 
    # Scale the numerical features
    print("\n values before scaling")
    print(self.dataset[dic[index]])
    self.dataset[dic[index]] = scaler.fit_transform(self.dataset[[dic[index]]])
    print("\n values after scaling")
    print(self.dataset[dic[index]])

   

  ################## encoding categorical features ####################
  def encoding_categorical(self):
    # Identify categorical features
    categorical_features = self.dataset.select_dtypes(include='object').columns.tolist()
    print('\n################ encoding ###############\n')
    print('\nchoose which categorical feature you need to encode')
    i=1
    dic={}
    print('{}-{}'.format(0,'back'))
    for col in  categorical_features:  
      print('{}-{}'.format(i,col))
      dic[i]=col
      i+=1 
     
    index1=int(input())
    print('choose the encoding type')
    index2=int(input('\n1-onehot encoding\n2-label encoding\n'))
    if index1==0:return
    if index1 not in range(len(categorical_features)+1):
      print('invalid choise')
      return
    if index2==1:
      # One-hot encoding
      onehot_encoder = OneHotEncoder(sparse_output=False)
      self.dataset[dic[index1]] = onehot_encoder.fit_transform(self.dataset[[dic[index1]]]) 
      print('\nafter encoding\n')
      print(self.dataset[dic[index1]])   
    elif index2==2:
      # Label encoding
      label_encoder = LabelEncoder()
      self.dataset[dic[index1]] = label_encoder.fit_transform(self.dataset[[dic[index1]]]) 
      print('after encoding\n')
      print(self.dataset[dic[index1]]) 
    else:print('invalid choise')


  ###################### scatter plots ########################
  def scatter(self):
    i=1
    dic={}
    print('\n##########  choose which columns you need to plot scatter to them  #################')
    num_cols=self.dataset.select_dtypes(include=['number']).columns.tolist()
    for col in  num_cols:  
      print('{}-{}'.format(i,col))
      dic[i]=col
      i+=1
    index1=int(input('X colmuns'))
    index2=int(input('Y colmuns'))
    plt.scatter(self.dataset[dic[index1]],self.dataset[dic[index2]])
    # Set x-axis label
    plt.xlabel(dic[index1])
    # Set y-axis label
    plt.ylabel(dic[index2])
    # Save the plot as an image file
    plt.savefig('plot.png')
    plt.close()
    # Display the saved image
    display(Image('plot.png'))



  #################### histogram plots ###########################
  def histogram(self):
    i=1
    dic={}
    print('\n######  choose which column you need to plot histogram  ###########')
    for col in  self.dataset.columns.tolist():  
      print('{}-{}'.format(i,col))
      dic[i]=col
      i+=1
    index=int(input())
    plt.hist(self.dataset[dic[index]],bins=20,edgecolor='white',linewidth=3)
    # Save the plot as an image file
    plt.title(dic[index])
    plt.savefig('plot.png')
    plt.close()
    # Display the saved image
    display(Image('plot.png'))


  ####################### pie charts ##################################
  def pie(self):
    i=1
    dic={}
    print('\n############  choose which column you need to plot pie chart  #################')
    for col in  self.dataset.columns.tolist():  
      print('{}-{}'.format(i,col))
      dic[i]=col
      i+=1
    index=int(input())
    count=self.dataset[dic[index]].value_counts()
    count=count[count>int(len(self.dataset)/150)]
    plt.pie(count.values,labels=count.index.values.tolist())
    # Save the plot as an image file
    plt.title(col)
    plt.savefig('plot.png')
    plt.close()
    # Display the saved image
    display(Image('plot.png'))
    

    


################################ running the code ############################
# Create the parser
parser = argparse.ArgumentParser(description='Tool Description')

# Add arguments/options
parser.add_argument('input_file', help='Path to the input file')
parser.add_argument('--output', '-o', help='Path to the output file')

# Parse the arguments
args = parser.parse_args()

# Access the values of the arguments
input_file = args.input_file
output_file = args.output

#reading the file
eda=EDA(input_file,input_file.split('.')[1])


# Perform operations based on the provided inputs
print('\n############ columns data types #################\n')
print(eda.col_dtypes()) 
print("\n\n")

while True :
  print('############ choose service  ###############')
  
  index1=int(input('\n1-pre-processing\n2-plotting\n3-Exit\n'))
  
  if index1==1:
    while True:
      index2=int(input('\n0-Back\n1-handling missing values\n2-remove duplicates\n3-scaling numerical values\n4-encoding categorical features\n'))
      if index2==1:
        eda.handling_missing_values()
      elif index2==2:
        eda.remove_duplicates()
      elif index2==3:
        eda.scaling_numerical_values()
      elif index2==4:
        eda.encoding_categorical()
      elif index2==0:break
      else:print('invalid choise')
  elif index1==2:
    while True:
      index3=int(input('\n######  choose which plot you want  #########\n1-histogram\n2-pie chart\n3-scatter\n4-BACK\n'))
      if index3==1:
        eda.histogram()
      elif index3==2:
        eda.pie()
      elif index3==3:
        eda.scatter()
      elif index3==4:break
      else:
        print('invalid choise')
  elif index1==3:break
  else:print('invalid choise')














