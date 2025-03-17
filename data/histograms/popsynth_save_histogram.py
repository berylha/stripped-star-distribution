
import numpy as np
import pandas as pd
from glob import glob

# --- CHOOSE THE FOLDER/METALLICITY HERE --------------------------------------
# Z0002, Z002, Z006, OR Z014
Z = 'Z014'
# -----------------------------------------------------------------------------

fnames = sorted(glob(f'../population_synthesis_runs/{Z}/data1_{Z}_*.txt'))

bins = np.geomspace(1, 50, 1000)

for i, fname in enumerate(fnames):
    df = pd.read_csv(fname, sep=r'\s+', comment='#', header=0)

    # Get rid of single stars
    df = df[df.Evolution != 'single'].reset_index(drop=True)
    # Only keep stripped stars
    df = df[df.Star_state_m1 == 2].reset_index(drop=True)
    # Get rid of ones that should have merged but didn't
    should_have_merged = (df.Pinit < 2)
    didnt_merge = (df.Evolution != 'merger_HG') & (df.Evolution != 'merger_MS')
    df = df[~(should_have_merged & didnt_merge)].reset_index(drop=True)

    # save the histogram in the current directory
    f = open(f'hist_{Z}.txt', 'a')
    hst = np.histogram(df.star_mass_1, bins=bins)
    for val in hst[0]:
        f.write(f'{val} ')
    f.write('\n')
    f.close()
    print(f'Done with file {i}/100')
