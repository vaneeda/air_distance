import pandas as pd
import numpy as np
import sklearn.neighbors
from itertools import combinations
import argparse

p = argparse.ArgumentParser(description='')
p.add_argument('-n', type=int
               , help='integer between 2 and 10')
args = p.parse_args()


earth_radius= 6378 # km https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
places = pd.read_csv("places.csv")

if args.n:
   if not 2 <= args.n <= 10:
       raise argparse.ArgumentTypeError("Please enter an integer between 2 and 10")
   places = places.sample(n=args.n).sort_index()

#Convert latitudes and longitudes to radians to calculate the air distance
places[['lat_rad', 'long_rad']]= np.radians(places.loc[:,['Latitude','Longitude']])
dist = sklearn.neighbors.DistanceMetric.get_metric('haversine')
mat = pd.DataFrame(dist.pairwise(places[['lat_rad', 'long_rad']].to_numpy()) * earth_radius,
                   columns=places.Name.unique(), index=places.Name.unique())

# Create unique list of pairwise combinations
comb = combinations(places.index, 2)
res = [list(ele) for ele in list(comb)]
names = places["Name"].to_dict()
d = []
for i in res:
    d.append({"Place_1": names[i[0]], "Place_2": names[i[1]],
                        "Distance": mat[names[i[0]]][names[i[1]]]})
final = pd.DataFrame(d)
avg = final["Distance"].mean()
pd.options.display.float_format = '{: .1f}'.format
params=final.iloc[(final['Distance']-avg).abs().argsort()[:1]].to_string(header=False)
final["km"]= "km"

# Display results
print(final[["Place_1","Place_2","Distance", "km"]].to_string(header=False))
print("Average distance: {:.1f} km. Closest pair: {} - {} {} km".
      format(avg,params.split("  ")[1],params.split("  ")[2],params.split("  ")[3]))
