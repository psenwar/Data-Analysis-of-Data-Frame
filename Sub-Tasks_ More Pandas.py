# Data Cleaning And Visualisation  - Sub Task
 ''' 
Question 1 (20%)
Load the energy data from the file Energy Indicators.xls, which is a list of indicators of energy supply and renewable electricity production from the United Nations for the year 2013, and should be put into a DataFrame with the variable name of energy.

Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:

['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']

Convert Energy Supply to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as np.NaN values.

Rename the following list of countries (for use in later questions):

"Republic of Korea": "South Korea",
"United States of America": "United States",
"United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
"China, Hong Kong Special Administrative Region": "Hong Kong"

There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these,

e.g.

'Bolivia (Plurinational State of)' should be 'Bolivia',

'Switzerland17' should be 'Switzerland'.



Next, load the GDP data from the file world_bank.csv, which is a csv containing countries' GDP from 1960 to 2015 from World Bank. Call this DataFrame GDP.

Make sure to skip the header, and rename the following list of countries:

"Korea, Rep.": "South Korea", 
"Iran, Islamic Rep.": "Iran",
"Hong Kong SAR, China": "Hong Kong"



Finally, load the Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology from the file scimagojr-3.xlsx, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame ScimEn.

Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).

The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'].

This function returns a DataFrame with 20 columns and 15 entries.
'''
def answer_one():
    import pandas as pd
    import numpy as np
    import re
    
    energy = pd.read_excel('Energy Indicators.xls')
    energy = energy[16:243]
    energy.drop(energy.columns[0:2],axis=1,inplace=True)
    energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy['Energy Supply']=energy['Energy Supply']*1000000
    energy = energy.replace("...",np.NaN)
    country = []
    for i in energy['Country']:
            pattern = re.compile(r'\D+')
            Country1 = pattern.findall(i)
            newdata =''.join(Country1)
            loc = newdata.find('(')
            if loc >0:
                newdata = newdata[0:loc-1]
            else:
                newdata = newdata
            country.append(newdata.strip())
    energy['Country']=country
    energy.set_index(['Country'],inplace=True)
    country_name = {"Republic of Korea": "South Korea","United States of America": "United States", "United Kingdom of Great Britain and Northern Ireland": "United Kingdom", "China, Hong Kong Special Administrative Region": "Hong Kong"}
    energy.rename(index = country_name,inplace = True) 

    GDP = pd.read_csv('world_bank.csv',sep=',',skiprows = 4)
    country_name2 ={"Korea, Rep.": "South Korea","Iran, Islamic Rep.": "Iran", "Hong Kong SAR, China": "Hong Kong"}
    GDP['Country Name']=GDP['Country Name'].replace(country_name2)

    ScimEn = pd.read_excel('scimagojr-3.xlsx')

    df1 = pd.merge(pd.merge(ScimEn,energy,left_on='Country',right_index=True,how ='outer'),GDP,left_on='Country',right_on='Country Name',how ='outer')
    df = df1[['Country','Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    df.set_index(['Country'],inplace =True)
    df = df.loc[df['Rank'].isin([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])]
    df.sort_index(by = 'Rank', ascending = True,inplace = True)   
    
    return df

answer_one()
'''
Question 2 (6.6%)
The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?

This function should return a single number.
'''
%%HTML
<svg width="800" height="300">
  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />
  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />
  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />
  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>
  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>
</svg>
#Everything but this!
def answer_two():
    m1, m2 = energy.shape
    m3, m4 = GDP.shape
    m5, m6 = ScimEn.shape
    f1, f2 = answer_one().shape
    return (m1*m2 + m3*m4 + m5*m6 - f1*f2)

'''
Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by answer_one())
Question 3 (6.6%)
What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)

This function should return a Series named avgGDP with 15 countries and their average GDP sorted in descending order.
'''
def answer_three():
    Top15 = answer_one()
    avg = Top15[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']].mean(axis=1,skipna = True).sort_index(ascending = False)
    return avg
    '''
Question 4 (6.6%)
By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?

This function should return a single number.
'''
def answer_four():
    df = answer_one()
    avgGDP = answer_three()
    df['avgGDP']=avgGDP
    df.sort_index(by = 'avgGDP',ascending = False,inplace = True)
    change = df.ix[5]['2015']-df.ix[5]['2006']      
    return change
    
   ''' 
Question 5 (6.6%)
What is the mean Energy Supply per Capita?

This function should return a single number.
'''
import numpy as np
def answer_five():
    Top15 = answer_one()
    mean = np.average(Top15['Energy Supply per Capita'])
    return float(mean)
    
    '''
Question 6 (6.6%)
What country has the maximum % Renewable and what is the percentage?

This function should return a tuple with the name of the country and the percentage.
'''
def answer_six():
    Top15 = answer_one()
    maxm = Top15['% Renewable'].max()
    c_maxm = Top15[Top15['% Renewable'] == maxm].iloc[0].name
    return c_maxm, maxm
answer_six()   
    '''
Question 7 (6.6%)
Create a new column that is the ratio of Self-Citations to Total Citations. What is the maximum value for this new column, and what country has the highest ratio?

This function should return a tuple with the name of the country and the ratio.
'''
def ratio(row):
    row['ratio'] = row['Self-citations'] / row['Citations']
    return row

def answer_seven():
    Top15 = answer_one()
    new = Top15.apply(ratio, axis=1)
    m = float(np.max(new['ratio']))
    country = new[new['ratio'] == m].iloc[0].name
    return country, m
answer_seven()   
    '''
Question 8 (6.6%)
Create a column that estimates the population using Energy Supply and Energy Supply per capita. What is the third most populous country according to this estimate?

This function should return a single string value.
'''
def answer_eight():
    Top15 = answer_one()
    Top15['pop'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Top15.sort_values(by='pop',ascending = False,inplace = True)
    return Top15.ix[2].name

'''
Question 9 (6.6%)
Create a column that estimates the number of citable documents per person. What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the .corr() method, (Pearson's correlation).

This function should return a single number.
# Visualisation Part
(Optional: Use the built-in function plot9() to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)
'''
def answer_nine():
    Top15 = answer_one()
    Top15['pop'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Top15['citable documents per person'] = np.float64(Top15['Citable documents']/Top15['pop'])
    corr = Top15['citable documents per person'].corr(Top15['Energy Supply per Capita'])
    return corr
0.79400104354429457

#plot9() # Be sure to comment out plot9() before submitting the assignment!
'''
Question 10 (6.6%)
Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.

This function should return a series named HighRenew whose index is the country name sorted in ascending order of rank.
'''
def answer_ten():
    Top15 = answer_one()
    median = np.median(Top15['% Renewable'])
    for i in range(len(Top15)):
        if Top15.iloc[i]['% Renewable'] >= median:
            Top15.set_value(Top15.iloc[i].name, 'HighRenew', 1)
        else:
            Top15.set_value(Top15.iloc[i].name, 'HighRenew', 0)
    Top15 = Top15['HighRenew']
    Top15 = Top15.sort(inplace=False)
    return Top15
    '''
Question 11 (6.6%)
Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.

ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
This function should return a DataFrame with index named Continent ['Asia', 'Australia', 'Europe', 'North America', 'South America'] and columns ['size', 'sum', 'mean', 'std']
'''
def answer_eleven():
    Top15 = answer_one()
    return "ANSWER"
Question 12 (6.6%)
Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?

This function should return a Series with a MultiIndex of Continent, then the bins for % Renewable. Do not include groups with no countries.

def answer_twelve():
    Top15 = answer_one()
    return "ANSWER"
    '''
Question 13 (6.6%)
Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.

e.g. 317615384.61538464 -> 317,615,384.61538464

This function should return a Series PopEst whose index is the country name and whose values are the population estimate string.
'''
def answer_thirteen():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15 = Top15['PopEst']
    for i in range(len(Top15)):
        country = Top15.keys()[i]
        number = "{:,}".format((Top15.iloc[i]))
        Top15.replace(Top15.iloc[i], number, inplace=True)
    return Top15
    '''
Optional
Use the built in function plot_optional() to see an example visualization.
'''
def plot_optional():
    import matplotlib as plt
    %matplotlib inline
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. \
This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' \
2014 GDP, and the color corresponds to the continent.")
