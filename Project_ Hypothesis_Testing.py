import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


#Hypothesis: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (price_ratio=quarter_before_recession/recession_bottom)

#The following data files are available for this assignment:
#From the Zillow research data site there is housing data for the United States. In particular the datafile for all homes at a city level, City_Zhvi_AllHomes.csv, has median home sale prices at a fine grained level.
#From the Wikipedia page on college towns is a list of university towns in the United States which has been copy and pasted into the file university_towns.txt.
#From Bureau of Economic Analysis, US Department of Commerce, the GDP over time of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file gdplev.xls. For this assignment, only look at GDP data from the first quarter of 2000 onward.

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

# Data Cleaning 

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan","Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State","RegionName"]  )'''
    with open('university_towns.txt') as file:
        data = []
        for line in file:
            data.append(line[:-1])
    state_town = []
    for line in data:
        if line[-6:] == '[edit]':
            state = line[:-6]
        elif '(' in line:
            town = line[:line.index('(')-1]
            state_town.append([state,town])
        else:
            town = line
            state_town.append([state,town])
    state_college_df = pd.DataFrame(state_town,columns = ['State','RegionName'])
    return state_college_df

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    x = pd.ExcelFile('gdplev.xls')
    gdp = x.parse(skiprows=7)#skiprows=17,skip_footer=(38))
    gdp = gdp[['Unnamed: 4', 'Unnamed: 5']]
    gdp = gdp.loc[212:]
    gdp.columns = ['Quarter','GDP']
    gdp['GDP'] = pd.to_numeric(gdp['GDP'])
    quarters = []
    for i in range(len(gdp) - 2):
        if (gdp.iloc[i][1] > gdp.iloc[i+1][1] and (gdp.iloc[i+1][1] > gdp.iloc[i+2][1])):
            quarters.append(gdp.iloc[i][0])
    return quarters[0]   
        
    
 def get_recession_end():
    x = pd.ExcelFile('gdplev.xls')
    gdp = x.parse(skiprows=7)#skiprows=17,skip_footer=(38))
    gdp = gdp[['Unnamed: 4', 'Unnamed: 5']]
    gdp = gdp.loc[212:]
    gdp.columns = ['Quarter','GDP']
    gdp['GDP'] = pd.to_numeric(gdp['GDP'])
    quarters = []
    for i in range(len(gdp) - 2):
        if (gdp.iloc[i][1] < gdp.iloc[i+1][1] and (gdp.iloc[i+1][1] < gdp.iloc[i+2][1]) ):
            if(gdp.iloc[i][0]>'2008q3'):
                 quarters.append(gdp.iloc[i+2][0])
    return quarters[0]


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    x = pd.ExcelFile('gdplev.xls')
    gdp = x.parse(skiprows=7)#skiprows=17,skip_footer=(38))
    gdp = gdp[['Unnamed: 4', 'Unnamed: 5']]
    gdp = gdp.loc[212:]
    gdp.columns = ['Quarter','GDP']
    gdp['GDP'] = pd.to_numeric(gdp['GDP'])
    rec_start = get_recession_start()
    rec_end = get_recession_end()
    new_data = gdp[gdp['Quarter']>rec_start]
    return  new_data.loc[new_data['GDP'].idxmin()][0]


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    import pandas as pd
    house_df = pd.read_csv('City_Zhvi_AllHomes.csv')
    house_df['State'] = house_df['State'].map(states)
    house_df.set_index(['State','RegionName'],inplace = True)
    house_df = house_df.loc[:,'2000-01':]
    # creat new columns representing yearname and quarter as string
    # using list comprehensions
    new_columns = [str(x)+y for x in range(2000,2017) for y in ['q1','q2','q3','q4']]
    '''
    Alternate way:
    new_columns = []
    for x in range(2000,2017):
        for y in ['q1','q2' ,'q3','q4']:
            new_columns.append(str(x)+y)
        '''
    #dropping last column i.e 2016q4
    new_columns.pop()
    x=0
    for col in new_columns:
        house_df[col] = house_df.iloc[:,x:x+3].mean(axis=1)
        x = x+3
    house_df = house_df.loc[:,'2000q1':]
    return house_df

# Hypothesis Testing

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


def run_ttest():
    
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    start = get_recession_start()
    bottom = get_recession_bottom()
    housing_data = convert_housing_data_to_quarters()
    housing_data = housing_data.loc[:, start: bottom]
    housing_data.reset_index(inplace=True)
    
    
    housing_data['price_ratio'] = (housing_data[start] - housing_data[bottom]) / housing_data[start]
    
    uni_towns = get_list_of_university_towns()  
    uni_town_list = uni_towns['RegionName'].tolist()
    
    housing_data['isUniTown'] = housing_data.RegionName.apply(lambda x: x in uni_town_list)
    
    uni_data = housing_data[housing_data.isUniTown].copy().dropna()
    not_uni_data = housing_data[~housing_data.isUniTown].copy().dropna()

    p = ttest_ind(uni_data['price_ratio'], not_uni_data['price_ratio'])[1]
    different = p < 0.01   
    
    lower = 'university town' if uni_data['price_ratio'].mean() < not_uni_data['price_ratio'].mean() else 'non-university town'

    return (different, p, lower)



