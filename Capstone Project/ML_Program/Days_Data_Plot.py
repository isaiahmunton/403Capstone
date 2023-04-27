import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import time

# Read the CSV file and extract columns 2 and 3, skipping the first row
df = pd.read_csv('Clean_Data/CleanData.csv', usecols=[1, 2], skiprows=[0])

# Create a Basemap instance with the desired map projection
lon_min, lat_min = df.min()
lon_max, lat_max = df.max()
buffer = 1  # Adjust this value to set the buffer around the plotted points
m = Basemap(projection='mill', llcrnrlat=lat_min-buffer, urcrnrlat=lat_max+buffer,
            llcrnrlon=lon_min-buffer, urcrnrlon=lon_max+buffer)

# Plot the coastlines and country borders of the world
m.drawcoastlines()
m.drawcountries()

# Loop over the coordinates and plot them one by one
for i in range(len(df)):
    # Convert the GPS coordinates to map coordinates and plot them as a scatter plot
    x, y = m(df.iloc[i, 0], df.iloc[i, 1])
    m.scatter(x, y, s=10, c='red', marker='o', alpha=0.5)

    m.drawcoastlines()
    m.drawcountries()
    
    # Add a title to the plot
    plt.title('GPS Coordinates on a Map')
    
    # Show the plot without blocking the loop
    plt.show(block=False)
    
    # Give time for the plot to update before continuing with the loop
    plt.pause(0.00001)
    
    # Clear the plot for the next iteration
    plt.clf()


