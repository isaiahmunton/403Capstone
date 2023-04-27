import pandas as pd # This is used for going through the dataset csv.


# This section takes the data and time and longitude and latitude GPS coordinates from DirtyData.csv, cleans thems,
# and puts them into CleanData.csv.
df1 = pd.read_csv("Animal_Tracking_Test_Dataset/DirtyData.csv", usecols=[2, 3, 4], na_values=[""])

df1.dropna(subset=[df1.columns[1], df1.columns[2]], inplace=True)

df1 = df1.iloc[:, [0, 1, 2]]

df1.iloc[:, [1, 2]] = df1.iloc[:, [1, 2]].applymap(lambda x: format(x, '.3f'))

df1.to_csv("Clean_Data/CleanData.csv", index=False)

# This section takes the data from CleanData.csv and breaks it up into multiple csv files corresponding to the data's date stamp.
df2 = pd.read_csv("Clean_Data/CleanData.csv")

df2['timestamp'] = pd.to_datetime(df2['timestamp'], format='%Y-%m-%d %H:%M:%S')

groups = df2.groupby(df2['timestamp'].dt.date)

for name, group in groups:
    filename = f'Clean_Data/Days/{name}.csv'
    group.to_csv(filename, index=False)