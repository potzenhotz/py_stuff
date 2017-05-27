#!/bin/env python3

#-----------------------------------------------------------------------
# Modules for import
#-----------------------------------------------------------------------
import matplotlib.pyplot as plt  
import pandas as pd 


# Read the data into a pandas DataFrame.    
hb_df = pd.read_csv('/Users/Potzenhotz/data/final_data/data_mart.csv', sep=';')
  
# These are the "Tableau 20" colors as RGB.    
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)    
  
# You typically want your plot to be ~1.33x wider than tall. This plot is a rare    
# exception because of the number of lines being plotted on it.    
# Common sizes: (10, 7.5) and (12, 9)    
plt.figure(figsize=(12, 14))    

# Remove the plot frame lines. They are unnecessary chartjunk.    
ax = plt.subplot(111)    
ax.spines["top"].set_visible(False)    
ax.spines["bottom"].set_visible(False)    
ax.spines["right"].set_visible(False)    
ax.spines["left"].set_visible(False)    
  
# Ensure that the axis ticks only show up on the bottom and left of the plot.    
# Ticks on the right and top of the plot are generally unnecessary chartjunk.    
ax.get_xaxis().tick_bottom()    
ax.get_yaxis().tick_left()    
  
# Limit the range of the plot to only where the data is.    
# Avoid unnecessary whitespace.    
#plt.ylim(0, 90)    
#plt.xlim(1968, 2014)    
  
# Make sure your axis ticks are large enough to be easily read.    
# You don't want your viewers squinting to read your plot.    
#plt.yticks(range(0, 91, 10), [str(x) + "%" for x in range(0, 91, 10)], fontsize=14)    
#plt.xticks(fontsize=14)    
  
# Provide tick lines across the plot to help your viewers trace along    
# the axis ticks. Make sure that the lines are light and small so they    
# don't obscure the primary data lines.    
#for y in range(10, 91, 10):    
#    plt.plot(range(1968, 2012), [y] * len(range(1968, 2012)), "--", lw=0.5, color="black", alpha=0.3)    
  
# Remove the tick marks; they are unnecessary with the tick lines we just plotted.    
plt.tick_params(axis="both", which="both", bottom="off", top="off",    
                labelbottom="on", left="off", right="off", labelleft="on")    

# Now that the plot is prepared, it's time to actually plot the data!    
# Note that I plotted the majors in order of the highest % in the final year.    
majors = ['Einnahmen', 'Ausgaben']    
majors = ['Konsum', 'Firma']    
majors = hb_df.Kategorie.unique()

hb_df = hb_df[['Wertstellung', 'Ausgaben', 'Kategorie']]

hb_df['Wertstellung'] = pd.to_datetime(hb_df['Wertstellung'],format='%d.%m.%Y')
hb_df = hb_df.sort('Wertstellung')
hb_df.index = [hb_df['Wertstellung']]
#hb_df = hb_df.resample('M').sum()
#hb_df['Ausgaben'] = hb_df['Ausgaben'].cumsum()
hb_df = hb_df.groupby(["Kategorie", pd.Grouper(freq='M',key='Wertstellung')]).sum()

print(hb_df.unstack(level=0))
hb_df = hb_df.unstack(level=0)

print(hb_df.xs('Konsum', level='Kategorie', axis=1))


for rank, column in enumerate(majors):    
    # Plot each line separately with its own color, using the Tableau 20    
    # color set in order.    
    print(rank, column)
    #plt.plot(hb_df.Wertstellung.values,    
    plt.hist(hb_df.index,    
            #hb_df[column].values,    
            hb_df.xs(column, level='Kategorie', axis=1),
            lw=2.5, color=tableau20[rank])

# Finally, save the figure as a PNG.    
# You can also save it as a PDF, JPEG, etc.    
# Just change the file extension in this call.    
# bbox_inches="tight" removes all the extra whitespace on the edges of your plot.    
plt.savefig("/Users/Potzenhotz/data/final_data/hb_plot.png", bbox_inches="tight")  


#'''  
