# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 10:08:56 2016

@author: lchlebak
"""

import pandas as pd
import matplotlib.pyplot as plt

# The purpose of this calculation is to find the aggregate costs of premiums
# (as they current stand) in comparison to the new premiums and OOP costs. One
# assumption being made is that none of the current employees that have 'Family'
# or '2-Person' plans will qualify for a 'Parent-Child' plan.

# Convert information about current premium cost distribution among the employees
# of the Springfield school district into a dataframe.
df = pd.DataFrame.from_csv('/home/lchlebak/Springfield Health/Current Costs (Summary).csv')

# This concerns the 3 missing employees who have old JY plans with different
# rate breakdowns.
dis_out1 = df.ix["Single (Plan JY)"]["Total Premium"]*0.744
dis_out2 = df.ix["2-Person (Plan JY)"]["Total Premium"]*0.742
dis_out3 = df.ix["Family (Plan JY)"]["Total Premium"]*0.74

em_out1 = df.ix["Single (Plan JY)"]["Total Premium"] - dis_out1
em_out2 = df.ix["2-Person (Plan JY)"]["Total Premium"] - dis_out2
em_out3 = df.ix["Family (Plan JY)"]["Total Premium"] - dis_out3

# This calculates the total current cost to employees in terms of premiums.
em_total_cost = em_out1 + em_out2 + em_out3
for item in df.index:
    dn = df.ix[item]
    em_total_cost = em_total_cost + dn["Employee Premium"]*dn["Number of Employees (3 People Missing)"]

# This calculates the total current cost to the district in terms of premiums.
dis_total_cost = dis_out1 + dis_out2 + dis_out3
for item in df.index:
    dn = df.ix[item]
    dis_total_cost = dis_total_cost + dn["District Premium"]*dn["Number of Employees (3 People Missing)"]
 
# These csv files contain information about the new VEHI plans and OOP costs.
dh = pd.DataFrame.from_csv('/home/lchlebak/Springfield Health/VEHI 2018 Plan Comparisons (Premium Rates).csv')
ds = pd.DataFrame.from_csv('/home/lchlebak/Springfield Health/VEHI 2018 Plan Comparisons (Deductibles-Single).csv')
dm = pd.DataFrame.from_csv('/home/lchlebak/Springfield Health/VEHI 2018 Plan Comparisons (Deductibles-Multiple).csv')

# This calculates the total number of employees that have 'Single' plans.
single_total = 1 + df.ix["Single (Plan JY)"]["Number of Employees (3 People Missing)"] + \
df.ix["Single (VHP)"]["Number of Employees (3 People Missing)"]

# This calculates the total number of employees that have '2-Person' plans.
two_person_total = 1 + df.ix["2-Person (Plan JY)"]["Number of Employees (3 People Missing)"] + \
df.ix["2-Person (VHP)"]["Number of Employees (3 People Missing)"]

# This calculates the total number of employees that have 'Family' plans.
family_total = 1 + df.ix["Family (Plan JY)"]["Number of Employees (3 People Missing)"] + \
df.ix["Family (VHP)"]["Number of Employees (3 People Missing)"]

# This calculates the total cost for the new premiums based on the distribution
# of family plans among the employees.
new_total_premium = dh.ix["Single"]*single_total*12 + dh.ix["2-Person"]*two_person_total*12 + \
dh.ix["Family"]*family_total*12

# This calculates the total cost for the new maximum OOP total based on the
# distribution of family plans among the employees.
new_total_OOP = ds["Total OOP"]*single_total + dm["Total OOP"]*(two_person_total + \
family_total)

# We now create our stacked bar graph.

# We first set the percentage split we want for the new premiums and
# out-of-pocket limits.
m = .835

# This creates the figure 'f' with the subplots being the "bars" in the
# plot.
f, ax1 = plt.subplots(1, figsize=(10,5))

# This sets the width of the bars.
bar_width = 0.3

# This positions the left bar-boundaries.
bar_1 = [i+(1-bar_width) for i in range(5)]
bar_2 = [i for i in range(1,6)]

# This positions the x-axis tick marks.
tick_pos = [i for i in bar_2]
    
# This correctly places the District Premium amount on the graph.
ax1.bar(bar_1[0],
        # take the district premium
        dis_total_cost, 
        # set the width
        width=bar_width,
        # give the correct label
        label='District Premium', 
        # with alpha 0.5
        alpha=0.5, 
        # with color in (R,G,B) format
        color=(.2,.6,.2))
        
# This correctly places the Employee Premium amount on the graph.
ax1.bar(bar_2[0],
        # take the employee premium
        em_total_cost, 
        # set the width
        width=bar_width,
        # give the correct label
        label='Employee Premium', 
        # with alpha 0.5
        alpha=0.5, 
        # with color in (R,G,B) format
        color=(0,1,0))
        
# This correctly places the District New Premium amounts on the graph.
ax1.bar(bar_1[1:],
        # take the new premiums
        m*new_total_premium, 
        # set the width
        width=bar_width,
        # give the correct label
        label='District New Premium', 
        # with alpha 0.5
        alpha=0.5, 
        # with color in (R,G,B) format
        color=(1, 0, 0))
            
# This correctly places the Employee New Premium amounts on the graph.
ax1.bar(bar_2[1:],
        # take the new premiums
        (1-m)*new_total_premium, 
        # set the width
        width=bar_width,
        # give the correct label
        label='Employee New Premium', 
        # with alpha 0.5
        alpha=0.5, 
        # with color in (R,G,B) format
        color=(1, .2, 0))
            
# This correctly places the OOP Limit amounts on the graph.
ax1.bar(bar_1[1:],
        # take the new OOP limits
        new_total_OOP, 
        # set the width
        width=bar_width,
        # give the correct label
        label='OOP Limit',
        # with District New Premium below
        bottom = m*new_total_premium,
        # with alpha 0.5
        alpha=0.5, 
        # with color in (R,G,B) format
        color=(.6, .4, .4))

# These are the names of the different bars in our graph.        
names = ["Old Plan", "VEHI Platinum","VEHI Gold", "VEHI Gold CDHP",
        "VEHI Silver CDHP"]
        
# This sets the x ticks with names.
plt.xticks(tick_pos, names)

# This provides dotted lines that indicates how much money is being
# spent right now on premiums.
threshold1 = em_total_cost
ax1.plot([0., 5.5], [threshold1, threshold1], "k--")
    
threshold2 = dis_total_cost
ax1.plot([0., 5.5], [threshold2, threshold2], "k--")

# This gives the lables and legend.
ax1.set_ylabel("Total Cost")
ax1.set_xlabel("Health Plans")
plt.legend(bbox_to_anchor=(0., 1.01, 1., .06), loc=3,
           ncol=3, mode="expand", borderaxespad=0.)
           
# This gives a buffer around the edges.
plt.xlim([min(tick_pos)-bar_width, max(tick_pos)+bar_width])