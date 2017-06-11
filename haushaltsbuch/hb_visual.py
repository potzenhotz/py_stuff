#!/bin/env python3

#-----------------------------------------------------------------------
# Modules for import
#-----------------------------------------------------------------------
import matplotlib.pyplot as plt  
import pandas as pd 
import hb_functions as hb
from sqlalchemy import create_engine
import sys
import seaborn as sns
sns.set_style("whitegrid")
#sns.set_style("whitegrid", {'axes.grid' : False})

'''
#-----------------------------------------------------------------------
#Define database
#-----------------------------------------------------------------------
'''
haushaltsbuch_db = create_engine('sqlite:////Users/Potzenhotz/data/database/haushaltsbuch.db')

'''
-----------------------------------------------------------------------
 CORE: Read table
-----------------------------------------------------------------------
'''
print('Start reading tables')
mart_sql_query = 'select * from dm_konsum\
                    where Jahr = "2016" \
                    and Monat = "12";' 
loaded_dm_konsum = hb.read_sql(haushaltsbuch_db, mart_sql_query)
loaded_dm_konsum.set_index('index', inplace=True)
print(loaded_dm_konsum)

transpose_konsum_df = loaded_dm_konsum
transpose_konsum_df = transpose_konsum_df.drop('Jahr', 1)
transpose_konsum_df = transpose_konsum_df.drop('Monat', 1)
transpose_konsum_df = transpose_konsum_df.T
print(transpose_konsum_df)
print(transpose_konsum_df.columns)

f, ax = plt.subplots(figsize=(10, 6))

# Load the example car crash dataset

print(list(transpose_konsum_df))

# Plot the total crashes
sns.set_color_codes("pastel")
sns_plot = sns.barplot(x=transpose_konsum_df['Ausgaben'], y=transpose_konsum_df.index,
            label="Ausgaben", color="b")
for p in ax.patches:
    width = p.get_width()
    print(width)
    print(p.get_y())
    ax.text(width + 10,
            p.get_y()+p.get_height()/1.9,
            int(width),
            va = 'center' ) 

# Turn off tick labels
ax.set_xticklabels([])
# Turns off grid on the left Axis.
ax.grid(False)

# Add a legend and informative axis label
ax.legend(ncol=3, loc="lower right", frameon=False)
ax.set(ylabel="", xlabel="")
sns.despine(left=True, bottom=True)
# bbox_inches="tight" removes all the extra whitespace on the edges of your plot.    
plt.savefig("/Users/Potzenhotz/data/final_data/hb_plot.png", bbox_inches="tight")  
plt.savefig("/Users/Potzenhotz/data/final_data/hb_plot.png")  


