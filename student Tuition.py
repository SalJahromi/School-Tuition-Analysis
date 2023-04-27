#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


df = pd.read_csv("nces330_20.csv")
df


# In[7]:


#lets look at the most recent data (year 2021) and fees/tuition only 
df_yr2021_4Year_tuition = df[(df['Year'] == 2021) & (df['Expense'] == 'Fees/Tuition') & 
                             (df['Length'] == '4-year')]
df_yr2021_4Year_tuition


# In[8]:


df_yr2019_4Year_tuition = df[(df['Year'] == 2019) & (df['Expense'] == 'Fees/Tuition') & 
                                     (df['Length'] == '4-year')]
df_yr2019_4Year_tuition


# In[9]:


df_yr2019_4Year_tuition['Type'].unique()


# In[10]:


plt.hist(df_yr2021_4Year_tuition['Value'])
plt.title("Plot of Average Fee/Tuition")
plt.xlabel("Average Fee/Tuition of Schools")
plt.ylabel("Number of Schools")
plt.show()


# In[11]:


plt.boxplot(df_yr2021_4Year_tuition['Value'])
plt.show()


# In[14]:


plt.boxplot(df_yr2019_4Year_tuition['Value'])
plt.show()


# In[15]:


df_yr2021_avgTuit = df_yr2021_4Year_tuition['Value'].groupby([df.iloc[:,3]]).mean()
print("mean tuition of 4 year institutions in year 2021 is ",df_yr2021_avgTuit[0], ' usd')


# In[16]:


df_yr2019_avgTuit = df_yr2019_4Year_tuition['Value'].groupby([df.iloc[:,3]]).mean()
print('mean tuition of 4 year institutions in year 2019 is ', df_yr2019_avgTuit[0], ' usd')


# Statistical Study:
#     We have two means in this study. The mean of the average tution costs of 2019 and the mean of the average tuition cost of 2021.
#     
#     
#     Lets obtain a few more pieces of information necessary for completing a two-means hypothesis test. 

# In[17]:


df_yr2021_stdTuit = df_yr2021_4Year_tuition['Value'].std()
df_yr2019_stdTuit = df_yr2019_4Year_tuition['Value'].std()

df_yr2021_sampleSize = df_yr2021_4Year_tuition['Value'].count()
df_yr2019_sampleSize = df_yr2019_4Year_tuition['Value'].count()


# In[18]:


from tabulate import tabulate

info = {'Schools':['Post-Secondaries of 2021', 'Post-Secondaries of 2019'],
        'Sample Size' :[df_yr2021_sampleSize,df_yr2019_sampleSize],
        'Mean Tuition': [df_yr2021_avgTuit,df_yr2019_avgTuit ],
        'Sample STD':[df_yr2021_stdTuit,df_yr2019_stdTuit]}

print(tabulate(info, headers='keys', tablefmt='fancy_grid'))


# Since we do not have a population standard deviation, the best method of testing the two means would be with the use of the t-test.
#  - first, we will carry out an F test to see whether we should use a pooled or non-pooled t-test

# In[19]:


import math
import scipy.stats



print('null hypothesis : std1 = std2 \nalt hypothesis: std1 ')


# In[20]:


#the standard deviation of 2019
sa = df_yr2019_stdTuit
#the standard deviation of 2021
sb = df_yr2021_stdTuit

#F test
F = (sa)**2 / (sb)**2
round(F,3)

FcritVal = scipy.stats.f.ppf(q=1-.05, dfn=df_yr2019_sampleSize-1 , dfd=df_yr2021_sampleSize-1)
print('F test statistic is ', F, '\nThe F critical value is ', FcritVal)
print()
print('Since F > Fa/2, we reject null hypothesis. Therefore, we must conduct a non-pooled t-test')


# Creating the hypothesis. 
# 
# According to College Board articles, the USA experienced 1.8% - 8.3% increase to 4-year study tuiton, depending on the type of school. This is for the year 2021-2022.
# 
# Here, we will hypothesize that the schools in 2021 experienced an increase to their tuition compared to 2019. This likely being a result of inflation and the pandemic. 
# 
# H0: The tuition of schools in 2021 is the same as schools in 2019
# 
# H1: The tuition of schools in 2021 is higher than the schools in 2019.
# 
# Alpha = 0.05

# In[36]:


data_group1 = df_yr2021_4Year_tuition['Value'] 
data_group2 = df_yr2019_4Year_tuition['Value']
data_group1
data_group2
scipy.stats.ttest_ind(data_group1, data_group2, equal_var=False, alternative = 'greater')



# Now to obtain the critical value.
# The degrees of freedom will be 100 and critical level is 0.05

# In[37]:


scipy.stats.t.ppf(0.05, 100)


# To reject H0 of a right tail test, the test statistic must be bigger than critical value. 
# 
# Test statistic = 5.501718366600542
# Critical value = -1.6602343260657506
# t.s > ta
# 
# According to this test we can reject the null hypothesis. Therefore, the tuition cost of 4-year post-secondary schools in 2021 is greater than the ones in 2019. 
