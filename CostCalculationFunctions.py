# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 11:26:41 2016

@author: lchlebak
"""
import pandas as pd

def premium_savings(n=.835, old_family_type="Family", new_family_type="Family",
                    old_plan="VHP"):
# This is the amount of money left over once the employee and district pay the
# same total amount of the premium that they are currently paying. An assumption
# here is that 'n' is the percentage of the premium that the district currently
# covers.
                    
# 'old_family_type' options: "Single", "1-Dependent", "Family"
# 'new_family_type' options: "Single", "2-Person", "Parent-Child", "Family"
# 'old_plan' options: "VHP", "Comp", "Plan JY", "Old Plan JY"                  

    # These are the relevant data sets.
    df = pd.DataFrame.from_csv('/home/lchlebak/Springfield Health/VEHI 2018 Plan Comparisons (Premium Rates).csv')
    dg = pd.DataFrame.from_csv('/home/lchlebak/Springfield Health/Springfield 2016-2017 Plan Comparisons (Premiums).csv')
    
    # This calculates the yearly cost of the premiums for each of the new health
    # plans, given the 'new_family_type'.
    family_year = 12*df.ix[new_family_type]
    
    # This calculates the yearly cost of the premium to the employee for their
    # current health plan.
    family_old_eyear = 25*dg.ix[old_family_type]
    employee_current_cost = family_old_eyear.ix[old_plan]
    
    # This calculates the yearly cost of the premium to the district for the
    # employee's current health plan.
    family_old_year = n*family_old_eyear/(1-n)
    district_current_cost = family_old_year.ix[old_plan]
    
    # These are the savings on the premiums given the assumption that the
    # employee and district pay the same amount of money that they currently do.
    # Negative numbers represent savings.
    savings = family_year - employee_current_cost - district_current_cost
    
    return savings
    

def worst_case_extra_cost(n=.835, old_family_type="Family", new_family_type="Family",
                 old_plan="VHP"):
# This is the extra amount that employees will have to pay for the different
# health plans not counting the portion of the premium that they will continue
# to pay. This is the worst case scenario for costs. Assumptions include that
# employees will pay the remainder of the premium not covered by the district and
# that 'n' is the percentage of the premium currently covered by the district.
                 
# 'old_family_type' options: "Single", "1-Dependent", "Family"
# 'new_family_type' options: "Single", "2-Person", "Parent-Child", "Family"
# 'old_plan' options: "VHP", "Comp", "Plan JY", "Old Plan JY"     
    
    # These are the data sets containing deductible/out-of-pocket values.               
    ds = pd.DataFrame.from_csv('/home/lchlebak/Springfield Health/VEHI 2018 Plan Comparisons (Deductibles-Single).csv')
    dm = pd.DataFrame.from_csv('/home/lchlebak/Springfield Health/VEHI 2018 Plan Comparisons (Deductibles-Multiple).csv')
    
    # This calculates the maximum out-of-pocket costs based on 'new_family_type".
    total_extra = 0
    if new_family_type == "Single":
        total_extra = ds["Total OOP"]
    else:
        total_extra = dm["Total OOP"]
    
    # This gives the maximum cost to the employee in addition to the (not included)
    # premium costs.
    employee_max_cost = premium_savings(n, old_family_type, new_family_type, old_plan) + total_extra
    
    return employee_max_cost
    
