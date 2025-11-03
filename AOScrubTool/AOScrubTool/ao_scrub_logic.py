import os, glob, pandas as pd

def run_ao_scrub(path, key, group, tier, utility, market, status, output_folder,
                 Star1='GIS Team identified 15-20 contiguous buildable acres',
                 Star2='GIS Team identified 20-25 contiguous buildable acres',
                 Star3='GIS Team identified 25+ contiguous buildable acres'):
    files = glob.glob(os.path.join(path, '*.csv'))
    filtered_files = [f for f in files if key in os.path.basename(f)]
    if not filtered_files:
        raise ValueError(f'No files found containing "{key}" in folder.')

    dfs = []
    for f in filtered_files:
        temp_df = pd.read_csv(f)
        dfs.append(temp_df)

    df = pd.concat(dfs, axis=0, ignore_index=True)

    df[["Email", "Phone", "Other Phone", "Mobile", "Site #", "ITC Adder"]] = ""
    df["Site Tier"] = tier
    df["Utility"] = utility
    df["Market"] = market
    df["Lead Status"] = status
    df["Group"] = market + '-' + group
    df["Site Lat/Long Coordinates"] = df["Latitude"].astype(str) + ";" + df["Longitude"].astype(str)
    df["Zip (Mailing Address)"] = df["Zip (Mailing Address)"].astype(str).str[:5]
    df["Nearest Substation"] = df["Nearest Substation"].astype(str) + " Unconfirmed"
    df["Distance to Nearest Substation (mi)"] = df["Distance to Nearest Substation (mi)"].astype(str) + " Radial"

    rename_map = {
        'Site County': 'County',
        'Asset Url': 'AO Link',
        'Star Rating': 'Description',
        'Robust Id (Reportall)': 'Robust ID',
        'Nearest Substation': 'Substation',
        'Distance to Nearest Substation (mi)': 'Distance to Substation',
        'City (Mailing Address)': 'City',
        'State (Mailing Address)': 'State',
        'Zip (Mailing Address)': 'Zip/Postal Code',
        'Buildable Area (Acres) (acre)': 'Buildable Area (Acres)',
        'Lot Size (acre)': 'Lot Size'
    }
    df.rename(columns=rename_map, inplace=True)

    df = df.replace({"Description": {1: Star1, 2: Star2, 3: Star3}})

    df = df.sort_values(by=['AO Project', 'Last Name', 'Company', 'First Name'])
    df = df.reset_index(drop=True)
    df['Site #'] = [f"{market}-{group}{str(i+1).zfill(3)}" for i in range(len(df))]

    desired_cols = [
        'First Name','Last Name','Company','Site Address','Site City','Site State','Site Zip Code',
        'APN/PIN','Site Municipal','County','Buildable Area (Acres)','Lot Size','Street',
        'Address Line 2','City','State','Zip/Postal Code','Phone','Other Phone','Mobile','Email',
        'AO Project','Group','Site #','AO Link','Site Tier','Utility','Market','Lead Status',
        'ITC Adder','Description','Site Lat/Long Coordinates','Robust ID','Substation','Distance to Substation'
    ]
    existing_cols = [c for c in desired_cols if c in df.columns]
    df = df[existing_cols]

    filename = f"AO {market} Search {group} ({utility}) {tier}.csv"
    output_file = os.path.join(output_folder, filename)
    df.to_csv(output_file, index=False)
    return output_file
