"""
Create pytables containing the files
"""
import h5py
import tables
import polars as pl
import numpy as np

# %%
# Read the table
# meta_table = pl.read_csv("table.csv")

# TODO PAULA: Add mechanism to sort z-stacks too
images_path = "images"
from pathlib import Path
from imageio import imread
field_names = ["img","mask"]
pathnames = {k:[] for k in field_names}
for key, scope_name in zip(field_names, ["araceli","phenix"]):
    for name in Path(images_path).glob("*.tiff"):
        if scope_name in str(name):
            pathnames[key].append(imread(name))

# Make them numpy arrays
tmp = {k:np.stack(v,dtype=np.float32)[np.newaxis,...] for k,v in pathnames.items()}
#  %%

for k,v in tmp.items():
    with tables.open_file('test.hdf', 'a') as f:
        try:
            ds = f.create_array(f.root, k, obj=v)
            ds[:] = v
        except Exception as e:
            print(e)


with tables.open_file('test.hdf', 'r') as f:
    print(f)
