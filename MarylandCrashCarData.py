#---------------------------------------------------------
# Collision groups against Injury Severity
#---------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("CrashReportingData.csv", low_memory=False)
# Converting to lower
df['Collision Type'] = df['Collision Type'].str.lower()

# Creating columns and group types of collisions
df.loc[df['Collision Type'].isin([
    'same dir rear end', 'front to rear'
]), 'Collision Group'] = 'rear end'

df.loc[df['Collision Type'].isin([
    'straight movement angle', 'angle', 'angle meets left turn',
    'angle meets right turn', 'angle meets left head on'
]), 'Collision Group'] = 'angle'

df.loc[df['Collision Type'].isin([
    'same direction sideswipe', 'sideswipe, same direction', 'opposite direction',
    'sideswipe', 'sideswipe, opposite direction', 'opposite direction sideswipe'
]), 'Collision Group'] = 'sideswipe'

df.loc[df['Collision Type'].isin([
    'single vehicle'
]), 'Collision Group'] = 'single_vehicle'

df.loc[df['Collision Type'].isin([
    "head on", 'front to front', 'head on left turn'
]), 'Collision Group'] = 'head_on'

df.loc[df['Collision Type'].isin([
    'same direction right turn', 'same direction left turn', 'same dir rend left turn',
    'same dir rend right turn', 'same dir both left turn', 'opposite dir both left turn'
]), 'Collision Group'] = 'turning'

df.loc[df['Collision Type'].isin([
    'other', 'unknown', 'rear to side', 'rear to rear'
]), 'Collision Group'] = 'other_unknown'

# Find rows where data is missing
missing = df[df['Collision Group'].isna()]
missing['Collision Type'].value_counts(dropna=False)

# Group collision group and injury severity
severity_by_collision = df.groupby(
    ['Collision Group', 'Injury Severity']
).size().unstack(fill_value=0)

# Horizontal graph
severity_by_collision.plot(kind='barh',
                           figsize=(12, 7),
                           edgecolor = "black")

plt.title("Injury Severity by Collision Group", fontsize=14)
plt.xlabel('Number of Crashes')
plt.ylabel("Collision Group")
plt.gca().set_facecolor('#f5ab76')
plt.gcf().set_facecolor('#f5ab76')

plt.legend(title='Injury Severity', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()



#--------------------------------------------------------------------------------
#Which vehicle makes and models appear most frequently in the crash dataset?
#--------------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("CrashReportingData.csv", low_memory=False)
# Find top 10 vehicle models
topModel = df['Vehicle Model'].value_counts().head(10)
# Find top 10 vehicle makes
topMakes = df['Vehicle Make'].value_counts().head(10)

# Find top makes and model combinations
top = df.groupby(['Vehicle Model', 'Vehicle Make']).size().sort_values(ascending=False).head(10)
print(top)

# Top 10 vehicle models
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#f5ab76')
ax.set_facecolor('#f5ab76')
colors = plt.colormaps['viridis'](range(10))
ax.barh(topModel.index, topModel.values, color=colors)
ax.set_title("Top 10 Vehicle Models in Crash Dataset")
ax.set_xlabel("Number of Crashes")
ax.set_ylabel("Vehicle Model")

plt.tight_layout()
plt.show()

# Top 10 vehicle makes
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_facecolor('#f5ab76')
fig.patch.set_facecolor('#f5ab76')
colors = plt.colormaps['cividis'](range(10))
ax.barh(topMakes.index, topMakes.values, color=colors)
ax.set_title("Top 10 Vehicle Makes in Crash Dataset")
ax.set_xlabel("Number of Crashes")
ax.set_ylabel("Vehicle Makes")

plt.tight_layout()
plt.show()


#--------------------------------------------
# Percentage of Crashes by driver at fault
#--------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("CrashReportingData.csv", low_memory=False)

# Count driver at fault values
fault = df['Driver At Fault'].value_counts()

plt.figure(figsize=(7, 7))
plt.gcf().set_facecolor('#f5ab76')
plt.pie(fault.values,
        labels=fault.index,
        autopct='%1.1f%%'
)
plt.title('Percentage of Crashes by Driver at Fault')
plt.show()


#--------------------------------------------
# Percentage of Crashes by driver at fault
#--------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("CrashReportingData.csv", low_memory=False)

# Convert "Crash Data/Time" column into an actual datetime format
df['Crash Date/Time'] = pd.to_datetime(df['Crash Date/Time'], errors='coerce')

# New year column
df['crashYear'] = df['Crash Date/Time'].dt.year

# Count crashes by agency and year
crashes = (df.groupby(['Agency Name', 'crashYear']).size().reset_index(name='crash_count'))

# Find the top 5 agencies
top = (crashes.groupby('Agency Name')['crash_count'].sum().nlargest(5).index)

plt.figure(figsize=(12, 7))
# Plot a line for each top agency
for agency in top:
  data = crashes[crashes['Agency Name'] == agency]

  plt.plot(data['crashYear'].astype(str),data['crash_count'],marker='o',label=agency)

plt.title('Crash Trends Over Time for Top Agencies')
plt.xlabel('Year')
plt.ylabel('Number of Crashes')
plt.xticks(rotation=45)
plt.gca().set_facecolor('#f5ab76')
plt.gcf().set_facecolor('#f5ab76')

plt.legend(title='Agency', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


#--------------------------------------
# Word Cloud of most common road names
#--------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

df = pd.read_csv("CrashReportingData.csv", low_memory = False)

# Count road name frequencies
df['Road Name'].value_counts().head(10)

topTen = df['Road Name'].value_counts().head(10)

newDict = topTen.to_dict()

wc = WordCloud(width = 800, height = 400)
wc = wc.generate_from_frequencies(newDict)

plt.figure(figsize = (10, 5))
plt.imshow(wc)
plt.axis('off')
plt.tight_layout()
plt.show()