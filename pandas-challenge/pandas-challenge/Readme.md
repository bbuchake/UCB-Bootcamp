

```python
#Add dependencies
import pandas as pd
import json

#Set path to data file
input_data = input("Please enter the path to data file: ")

#Get data
heroes_data = json.load(open(input_data))

#Create df
heroes_df = pd.DataFrame(heroes_data)
heroes_df.head()


```

    Please enter the path to data file: Data/purchase_data.json
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Age</th>
      <th>Gender</th>
      <th>Item ID</th>
      <th>Item Name</th>
      <th>Price</th>
      <th>SN</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>38</td>
      <td>Male</td>
      <td>165</td>
      <td>Bone Crushing Silver Skewer</td>
      <td>3.37</td>
      <td>Aelalis34</td>
    </tr>
    <tr>
      <th>1</th>
      <td>21</td>
      <td>Male</td>
      <td>119</td>
      <td>Stormbringer, Dark Blade of Ending Misery</td>
      <td>2.32</td>
      <td>Eolo46</td>
    </tr>
    <tr>
      <th>2</th>
      <td>34</td>
      <td>Male</td>
      <td>174</td>
      <td>Primitive Blade</td>
      <td>2.46</td>
      <td>Assastnya25</td>
    </tr>
    <tr>
      <th>3</th>
      <td>21</td>
      <td>Male</td>
      <td>92</td>
      <td>Final Critic</td>
      <td>1.36</td>
      <td>Pheusrical25</td>
    </tr>
    <tr>
      <th>4</th>
      <td>23</td>
      <td>Male</td>
      <td>63</td>
      <td>Stormfury Mace</td>
      <td>1.27</td>
      <td>Aela59</td>
    </tr>
  </tbody>
</table>
</div>



**Player Count**


```python
# Player Count
player_count = len(heroes_df["SN"].unique())
player_count_df = pd.DataFrame([{"Total Players": player_count}])
player_count_df.style
```




<style  type="text/css" >
</style>  
<table id="T_55996be4_22e8_11e8_a032_a44cc89e03e3" > 
<thead>    <tr> 
        <th class="blank level0" ></th> 
        <th class="col_heading level0 col0" >Total Players</th> 
    </tr></thead> 
<tbody>    <tr> 
        <th id="T_55996be4_22e8_11e8_a032_a44cc89e03e3level0_row0" class="row_heading level0 row0" >0</th> 
        <td id="T_55996be4_22e8_11e8_a032_a44cc89e03e3row0_col0" class="data row0 col0" >573</td> 
    </tr></tbody> 
</table> 



**Purchasing Analysis (Total)**


```python
#Purchasing Analysis (Total)

#Number of Unique Items
unique_items = len(heroes_df["Item ID"].unique())

#Average Purchase Price
average_purchase_price = round(heroes_df["Price"].mean(),2)

#Total Number of Purchases
total_purchases = len(heroes_df.index)

#Total Revenue
total_revenue = round(heroes_df["Price"].sum(),2)

purchasing_analysis_df = pd.DataFrame([{"Number of Unique Items": unique_items, 
                                       "Average Price": average_purchase_price,
                                       "Number of Purchases": total_purchases,
                                       "Total Revenue": total_revenue}])
purchasing_analysis_df.style
```




<style  type="text/css" >
</style>  
<table id="T_55a2d252_22e8_11e8_84f7_a44cc89e03e3" > 
<thead>    <tr> 
        <th class="blank level0" ></th> 
        <th class="col_heading level0 col0" >Average Price</th> 
        <th class="col_heading level0 col1" >Number of Purchases</th> 
        <th class="col_heading level0 col2" >Number of Unique Items</th> 
        <th class="col_heading level0 col3" >Total Revenue</th> 
    </tr></thead> 
<tbody>    <tr> 
        <th id="T_55a2d252_22e8_11e8_84f7_a44cc89e03e3level0_row0" class="row_heading level0 row0" >0</th> 
        <td id="T_55a2d252_22e8_11e8_84f7_a44cc89e03e3row0_col0" class="data row0 col0" >2.93</td> 
        <td id="T_55a2d252_22e8_11e8_84f7_a44cc89e03e3row0_col1" class="data row0 col1" >780</td> 
        <td id="T_55a2d252_22e8_11e8_84f7_a44cc89e03e3row0_col2" class="data row0 col2" >183</td> 
        <td id="T_55a2d252_22e8_11e8_84f7_a44cc89e03e3row0_col3" class="data row0 col3" >2286.33</td> 
    </tr></tbody> 
</table> 



**Gender Demographics**


```python
#Gender Demographics
gender_names = heroes_df["Gender"].value_counts().keys().tolist() #gender names list
gender_counts = heroes_df["Gender"].value_counts().tolist() #gender counts list
gender_percents = [round((gc/total_purchases)*100,2) for gc in gender_counts] #gender percents list

#Percentage and Count of Male Players
#Percentage and Count of Female Players
#Percentage and Count of Other / Non-Disclosed
gender_demo_df = pd.DataFrame({"Percentage of Players": gender_percents, 
                               "Total Counts": gender_counts})
gender_demo_df.index = gender_names
gender_demo_df.head()

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Percentage of Players</th>
      <th>Total Counts</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>81.15</td>
      <td>633</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>17.44</td>
      <td>136</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>1.41</td>
      <td>11</td>
    </tr>
  </tbody>
</table>
</div>



**Purchasing Analysis (Gender)** 


```python
#The below each broken by gender
gender_grouped = heroes_df.groupby(["Gender"])

#Purchase Count
gender_purchase_count = gender_grouped["Item ID"].count()

#Average Purchase Price
gender_avg_price = round(gender_grouped["Price"].mean(),2)

#Total Purchase Value
gender_total_purchase = round(gender_grouped["Price"].sum(),2)

#Normalized Total
gender_normalized_count = pd.DataFrame(gender_grouped["SN"].unique()).SN.apply(lambda x: len(x))

gender_normalized_total = round(gender_grouped["Price"].sum()/gender_normalized_count,2)

gender_analysis_df = pd.DataFrame({"Purchase Count": gender_purchase_count, 
                                  "Average Purchase Price": gender_avg_price,
                                    "Total Purchase Value": gender_total_purchase,
                                    "Normalized Totals": gender_normalized_total})
gender_analysis_df.index = gender_names
gender_analysis_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Purchase Price</th>
      <th>Normalized Totals</th>
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>2.82</td>
      <td>3.83</td>
      <td>136</td>
      <td>382.91</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>2.95</td>
      <td>4.02</td>
      <td>633</td>
      <td>1867.68</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>3.25</td>
      <td>4.47</td>
      <td>11</td>
      <td>35.74</td>
    </tr>
  </tbody>
</table>
</div>



**Age Demographics**


```python
#Age Demographics

heroes_df["Age Range"] = pd.cut(heroes_df["Age"], [0, 9, 14, 19, 24, 29, 34, 39, 100], 
                                labels=["<10", "10-14", "15-19", "20-24", 
                                "25-29", "30-34", "35-39", "40+"])
age_names = heroes_df["Age Range"].value_counts().keys().tolist()#age range names list
age_counts = heroes_df["Age Range"].value_counts().tolist() #age counts list
age_percents = [round((ac/total_purchases)*100,2) for ac in age_counts] #age percents list

#Percentage and Count of Age Ranges
age_demo_df = pd.DataFrame({"Percentage of Players": age_percents, 
                               "Total Counts": age_counts})
age_demo_df.index = age_names
age_demo_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Percentage of Players</th>
      <th>Total Counts</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>20-24</th>
      <td>43.08</td>
      <td>336</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>17.05</td>
      <td>133</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>16.03</td>
      <td>125</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>8.21</td>
      <td>64</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>5.38</td>
      <td>42</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>4.49</td>
      <td>35</td>
    </tr>
    <tr>
      <th>&lt;10</th>
      <td>3.59</td>
      <td>28</td>
    </tr>
    <tr>
      <th>40+</th>
      <td>2.18</td>
      <td>17</td>
    </tr>
  </tbody>
</table>
</div>




```python
#The below each broken into bins of 4 years (i.e. &lt;10, 10-14, 15-19, etc.) 

age_grouped = heroes_df.groupby(["Age Range"])

#Purchase Count
age_purchase_count = age_grouped["Item ID"].count()

#Average Purchase Price
age_avg_price = round(age_grouped["Price"].mean(),2)

#Total Purchase Value
age_total_purchase = round(age_grouped["Price"].sum(),2)

#Normalized Total
age_normalized_count = pd.DataFrame(age_grouped["SN"].unique()).SN.apply(lambda x: len(x))
age_normalized_total = round(age_grouped["Price"].sum()/age_normalized_count,2)

age_analysis_df = pd.DataFrame({"Purchase Count": age_purchase_count, 
                                "Average Purchase Price": age_avg_price,
                                "Total Purchase Value": age_total_purchase,
                                "Normalized Totals": age_normalized_total})
age_analysis_df.index = age_names
age_analysis_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Purchase Price</th>
      <th>Normalized Totals</th>
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>20-24</th>
      <td>2.98</td>
      <td>4.39</td>
      <td>28</td>
      <td>83.46</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>2.77</td>
      <td>4.22</td>
      <td>35</td>
      <td>96.95</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>2.91</td>
      <td>3.86</td>
      <td>133</td>
      <td>386.42</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>2.91</td>
      <td>3.78</td>
      <td>336</td>
      <td>978.77</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>2.96</td>
      <td>4.26</td>
      <td>125</td>
      <td>370.33</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>3.08</td>
      <td>4.20</td>
      <td>64</td>
      <td>197.25</td>
    </tr>
    <tr>
      <th>&lt;10</th>
      <td>2.84</td>
      <td>4.42</td>
      <td>42</td>
      <td>119.40</td>
    </tr>
    <tr>
      <th>40+</th>
      <td>3.16</td>
      <td>4.89</td>
      <td>17</td>
      <td>53.75</td>
    </tr>
  </tbody>
</table>
</div>



**Top Spenders**


```python
#Identify the the top 5 spenders in the game by total purchase value, then list (in a table):
#SN
sn_grouped = heroes_df.groupby(["SN"])

#Purchase Count
sn_purchase_count = sn_grouped["Item ID"].count()

#Average Purchase Price
sn_avg_price = round(sn_grouped["Price"].mean(),2)

#Total Purchase Value
sn_total_purchase = round(sn_grouped["Price"].sum(),2)

sn_analysis_df = pd.DataFrame({"Purchase Count": sn_purchase_count, 
                               "Average Purchase Price": sn_avg_price,
                                "Total Purchase Value": sn_total_purchase})
sn_analysis_df.index = heroes_df.groupby(["SN"]).groups.keys()

#Get top 5 elements
sn_analysis_df.sort_values(["Total Purchase Value"], ascending=[False], inplace=True)
sn_analysis_df.head(5)

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Purchase Price</th>
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Undirrala66</th>
      <td>3.41</td>
      <td>5</td>
      <td>17.06</td>
    </tr>
    <tr>
      <th>Saedue76</th>
      <td>3.39</td>
      <td>4</td>
      <td>13.56</td>
    </tr>
    <tr>
      <th>Mindimnya67</th>
      <td>3.18</td>
      <td>4</td>
      <td>12.74</td>
    </tr>
    <tr>
      <th>Haellysu29</th>
      <td>4.24</td>
      <td>3</td>
      <td>12.73</td>
    </tr>
    <tr>
      <th>Eoda93</th>
      <td>3.86</td>
      <td>3</td>
      <td>11.58</td>
    </tr>
  </tbody>
</table>
</div>



**Most Popular Items**


```python
#Identify the 5 most popular items by purchase count, then list (in a table):
 #Item ID
 #Item Name
 #Purchase Count
 #Item Price
 #Total Purchase Value
item_grouped = heroes_df.groupby(["Item ID", "Item Name"])

#Purchase Count
item_purchase_count = item_grouped["Item ID"].count()

#Average Purchase Price
item_avg_price = round(item_grouped["Price"].mean(),2)

#Total Purchase Value
item_total_purchase = round(item_grouped["Price"].sum(),2)

item_analysis_df = pd.DataFrame({"Purchase Count": item_purchase_count, 
                               "Average Purchase Price": item_avg_price,
                                "Total Purchase Value": item_total_purchase})

#Get top 5 elements
item_analysis_df.sort_values(["Purchase Count"], ascending=[False], inplace=True)
item_analysis_df.head(5)
    
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>Average Purchase Price</th>
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th>Item Name</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>39</th>
      <th>Betrayal, Whisper of Grieving Widows</th>
      <td>2.35</td>
      <td>11</td>
      <td>25.85</td>
    </tr>
    <tr>
      <th>84</th>
      <th>Arcane Gem</th>
      <td>2.23</td>
      <td>11</td>
      <td>24.53</td>
    </tr>
    <tr>
      <th>31</th>
      <th>Trickster</th>
      <td>2.07</td>
      <td>9</td>
      <td>18.63</td>
    </tr>
    <tr>
      <th>175</th>
      <th>Woeful Adamantite Claymore</th>
      <td>1.24</td>
      <td>9</td>
      <td>11.16</td>
    </tr>
    <tr>
      <th>13</th>
      <th>Serenity</th>
      <td>1.49</td>
      <td>9</td>
      <td>13.41</td>
    </tr>
  </tbody>
</table>
</div>



**Most Profitable Items**


```python
#Identify the 5 most profitable items by total purchase value, then list (in a table):
item_analysis_df.sort_values(["Total Purchase Value"], ascending=[False], inplace=True)
item_analysis_df.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>Average Purchase Price</th>
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th>Item Name</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>34</th>
      <th>Retribution Axe</th>
      <td>4.14</td>
      <td>9</td>
      <td>37.26</td>
    </tr>
    <tr>
      <th>115</th>
      <th>Spectral Diamond Doomblade</th>
      <td>4.25</td>
      <td>7</td>
      <td>29.75</td>
    </tr>
    <tr>
      <th>32</th>
      <th>Orenmir</th>
      <td>4.95</td>
      <td>6</td>
      <td>29.70</td>
    </tr>
    <tr>
      <th>103</th>
      <th>Singed Scalpel</th>
      <td>4.87</td>
      <td>6</td>
      <td>29.22</td>
    </tr>
    <tr>
      <th>107</th>
      <th>Splitter, Foe Of Subtlety</th>
      <td>3.61</td>
      <td>8</td>
      <td>28.88</td>
    </tr>
  </tbody>
</table>
</div>


