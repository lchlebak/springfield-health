# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 19:30:44 2016

@author: lchlebak
"""


import pandas as pd
import matplotlib.pyplot as plt

def split_cost_bar_graph(n=.835, old_family_type="Family", new_family_type="Family",
                    old_plan="VHP"):
# This provides a stacked bar graph showing the total amount currently paid in
# terms of premiums, subdivided into the employee and district contributions,
# compared to the amount of worst-case-scenario costs of premiums
# and out-of-pocket limits. The new premiums and out-of-pocket
# costs are then split between the employee and district according to a set
# m=.835 percentage.
                    
# 'n' options: for "Plan JY Family", .8 and .74; for "PLan JY Single", .8 and .744;
# for "Plan JY 2-Person", .8 and .742; for "VHP", .835               
# 'old_family_type' options: "Single", "2-Person", "Family"
# 'new_family_type' options: "Single", "2-Person", "Parent-Child", "Family"
# 'old_plan' options: "VHP", "Plan JY"     

    # These are the relevant data regarding premiums.
    df = pd.DataFrame.from_csv('/home/lchlebak/Springfield Health/VEHI 2018 Plan Comparisons (Premium Rates).csv')
    dg = pd.DataFrame.from_csv('/home/lchlebak/Springfield Health/Current Costs.csv')

    # This is the total premium amount for the new health plans, given the
    # 'new_family_type'.
    family_year = 12*df.ix[new_family_type]

    # This is the total premium amount that the employee currently pays.
    family_old_eyear = 12*(1-n)*dg.ix[old_family_type]
    employee_current_cost = family_old_eyear.ix[old_plan]

    # This is the total premium amount that the district current pays for the
    # employee.
    family_old_dyear = 12*n*dg.ix[old_family_type]
    district_current_cost = family_old_dyear.ix[old_plan]

    # These are the data sets containing deductible/out-of-pocket values.               
    ds = pd.DataFrame.from_csv('/home/lchlebak/Springfield Health/VEHI 2018 Plan Comparisons (Deductibles-Single).csv')
    dm = pd.DataFrame.from_csv('/home/lchlebak/Springfield Health/VEHI 2018 Plan Comparisons (Deductibles-Multiple).csv')
    
    # This calculates the maximum out-of-pocket costs based on 'new_family_type".
    if new_family_type == "Single":
        OOP_limit = ds["Total OOP"]
    else:
        OOP_limit = dm["Total OOP"]

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
            district_current_cost, 
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
            employee_current_cost, 
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
            m*family_year, 
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
            (1-m)*family_year, 
            # set the width
            width=bar_width,
            # give the correct label
            label='Employee New Premium', 
            # with alpha 0.5
            alpha=0.5, 
            # with color in (R,G,B) format
            color=(1, .2, 0))
            
    # This correctly places the District OOP Limit amounts on the graph.
    ax1.bar(bar_1[1:],
            # take the new OOP limits
            m*OOP_limit, 
            # set the width
            width=bar_width,
            # give the correct label
            label='District OOP Limit',
            # with District New Premium below
            bottom = m*family_year,
            # with alpha 0.5
            alpha=0.5, 
            # with color in (R,G,B) format
            color=(.6, .4, .4))
    
    # This correctly places the Employee OOP Limit amounts on the graph.
    ax1.bar(bar_2[1:],
            # take the new OOP limits
            (1-m)*OOP_limit, 
            # set the width
            width=bar_width,
            # give the correct label
            label='Employee OOP Limit',
            # with Employee New Premium below
            bottom = (1-m)*family_year,
            # with alpha 0.5
            alpha=0.5, 
            # with color in (R,G,B) format
            color=(.6, .6, .4))

    # These are the names of the different bars in our graph.        
    names = ["Old Plan", "VEHI Platinum","VEHI Gold", "VEHI Gold CDHP",
             "VEHI Silver CDHP"]
        
    # This sets the x ticks with names.
    plt.xticks(tick_pos, names)

    # This provides dotted lines that indicates how much money is being
    # spent right now on premiums.
    threshold1 = employee_current_cost
    ax1.plot([0., 5.5], [threshold1, threshold1], "k--")
    
    threshold2 = district_current_cost
    ax1.plot([0., 5.5], [threshold2, threshold2], "k--")

    # This gives the lables and legend.
    ax1.set_ylabel("Total Cost")
    ax1.set_xlabel("Health Plans")
    plt.legend(bbox_to_anchor=(0., 1.01, 1., .06), loc=3,
           ncol=3, mode="expand", borderaxespad=0.)
           
    # This gives a buffer around the edges.
    plt.xlim([min(tick_pos)-bar_width, max(tick_pos)+bar_width])
    
    # Make a dataframe of the new costs and turn it into a csv file.  
    frames = [m*family_year, (1-m)*family_year, m*OOP_limit, (1-m)*OOP_limit]
    result = pd.concat(frames, axis=1)
    result.columns = ["District New Premium", "Employee New Premium",
                      "District OOP Limit", "Employee OOP Limit"]
    result.to_csv("SplitCostBarGraph"+old_family_type+new_family_type+old_plan+".csv")
    
    # This returns the bar graph.
    return "See graph in new window."