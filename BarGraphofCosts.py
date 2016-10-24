# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 09:39:00 2016

@author: lchlebak
"""

import pandas as pd
import matplotlib.pyplot as plt

def cost_bar_graph(n=.835, old_family_type="Family", new_family_type="Family",
                    old_plan="VHP"):
# This provides a stacked bar graph showing the total amount current paid in
# terms of premiums (subdivided into the employee and district contributions)
# compared to the amount of worst-case-scenario costs of premiums, deductibles,
# and out-of-pocket limits.
                    
# 'old_family_type' options: "Single", "1-Dependent", "Family"
# 'new_family_type' options: "Single", "2-Person", "Parent-Child", "Family"
# 'old_plan' options: "VHP", "Comp", "Plan JY", "Old Plan JY"     

    # These are the relevant data regarding premiums.
    df = pd.DataFrame.from_csv('/home/lchlebak/Springfield Health/VEHI 2018 Plan Comparisons (Premium Rates).csv')
    dg = pd.DataFrame.from_csv('/home/lchlebak/Springfield Health/Springfield 2016-2017 Plan Comparisons (Premiums).csv')

    # This is the total premium amount for the new health plans, given the
    # 'new_family_type'.
    family_year = 12*df.ix[new_family_type]

    # This is the total premium amount that the employee currently pays.
    family_old_eyear = 25*dg.ix[old_family_type]
    employee_current_cost = family_old_eyear.ix[old_plan]

    # This is the total premium amount that the district current pays for the
    # employee.
    family_old_year = n*family_old_eyear/(1-n)
    district_current_cost = family_old_year.ix[old_plan]

    # These are the data sets containing deductible/out-of-pocket values.               
    ds = pd.DataFrame.from_csv('/home/lchlebak/Springfield Health/VEHI 2018 Plan Comparisons (Deductibles-Single).csv')
    dm = pd.DataFrame.from_csv('/home/lchlebak/Springfield Health/VEHI 2018 Plan Comparisons (Deductibles-Multiple).csv')
    
    # This calculates the maximum deductible and out-of-pocket costs based on
    # 'new_family_type".
    if new_family_type == "Single":
        deductible = ds["Total Deductible"]
        OOP_limit = ds["Total OOP"]
    else:
        deductible = dm["Total Deductible"]
        OOP_limit = dm["Total OOP"]

    # We now create our stacked bar graph.

    # This creates the figure 'f' with the subplots being the "bars" in the
    # plot.
    f, ax1 = plt.subplots(1, figsize=(10,5))

    # This sets the width of the bars.
    bar_width = 0.6

    # This positions the left bar-boundaries.
    bar_1 = [i+(bar_width/2) for i in range(5)]

    # This positions the x-axis tick marks.
    tick_pos = [i+(bar_width/2) for i in bar_1]

    # This correctly places the Employee Premium amount on the graph.
    ax1.bar(bar_1[0],
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
        
    # This correctly places the District Premium amount on the graph.
    ax1.bar(bar_1[0],
            # take the district premium
            district_current_cost, 
            # set the width
            width=bar_width,
            # give the correct label
            label='District Premium', 
            # with Employee Premium below
            bottom = employee_current_cost,
            # with alpha 0.5
            alpha=0.5, 
            # with color in (R,G,B) format
            color=(.2,.6,.2))
    
    # This correctly places the New Premium amounts on the graph.
    ax1.bar(bar_1[1:],
            # take the new premiums
            family_year, 
            # set the width
            width=bar_width,
            # give the correct label
            label='New Premium', 
            # with alpha 0.5
            alpha=0.5, 
            # with color in (R,G,B) format
            color=(1, 0, 0))

    # This correctly places the Deductible amounts on the graph.        
    ax1.bar(bar_1[1:],
            # take the new deductibles
            deductible, 
            # set the width
            width=bar_width,
            # give the correct label
            label='Deductible', 
            # with New Premium below
            bottom = family_year,
            # with alpha 0.5
            alpha=0.5, 
            # with color in (R,G,B) format
            color=(.8, .2, .2))
    
    # This correctly places the OOP Limit amounts on the graph.
    ax1.bar(bar_1[1:],
            # take the new OOP limits
            OOP_limit, 
            # set the width
            width=bar_width,
            # give the correct label
            label='OOP Limit',
            # with New Premium and Deductible below
            bottom = family_year + deductible,
            # with alpha 0.5
            alpha=0.5, 
            # with color in (R,G,B) format
            color=(.6, .4, .4))

    # These are the names of the different bars in our graph.        
    names = ["Old Plan", "VEHI Platinum","VEHI Gold", "VEHI Gold CDHP",
             "VEHI Silver CDHP"]
        
    # This sets the x ticks with names.
    plt.xticks(tick_pos, names)

    # This provides a dotted line that indicates how much money is being
    # spent right now on premiums.
    threshold = employee_current_cost + district_current_cost
    ax1.plot([0., 5.], [threshold, threshold], "k--")

    # This gives the lables and legend.
    ax1.set_ylabel("Total Cost")
    ax1.set_xlabel("Health Plans")
    plt.legend(loc='lower right')

    # This gives a buffer around the edges.
    plt.xlim([min(tick_pos)-bar_width, max(tick_pos)+bar_width])
    
    # This returns the bar graph.
    return "See bar graph in new window."
