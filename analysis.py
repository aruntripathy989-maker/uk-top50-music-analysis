import pandas as pd
import numpy as np

def load_data(filepath="Atlantic_United_Kingdom.csv"):
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip().str.lower()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['artist'] = df['artist'].str.strip()
    df['is_explicit'] = df['is_explicit'].astype(bool)
    df['duration_min'] = df['duration_ms'] / 60000
    df['is_collab'] = df['artist'].str.contains('&|feat|ft\.', case=False, na=False)
    return df

def artist_dominance(df):
    appearances = df['artist'].value_counts().reset_index()
    appearances.columns = ['artist', 'appearances']
    total = len(df)
    top5_share = appearances.head(5)['appearances'].sum() / total * 100
    artist_concentration_index = round(top5_share, 2)
    return appearances, artist_concentration_index

def collaboration_analysis(df):
    collab_count = df['is_collab'].sum()
    solo_count = len(df) - collab_count
    collab_ratio = round(collab_count / len(df) * 100, 2)
    top10 = df[df['position'] <= 10]
    top10_collab = round(top10['is_collab'].sum() / len(top10) * 100, 2)
    return collab_count, solo_count, collab_ratio, top10_collab

def explicit_analysis(df):
    explicit_share = round(df['is_explicit'].sum() / len(df) * 100, 2)
    explicit_by_rank = df.groupby('is_explicit')['position'].mean().reset_index()
    return explicit_share, explicit_by_rank

def album_analysis(df):
    if 'album_type' in df.columns:
        album_dist = df['album_type'].value_counts().reset_index()
        album_dist.columns = ['album_type', 'count']
    else:
        album_dist = pd.DataFrame({'album_type': ['Unknown'], 'count': [0]})
    return album_dist

def duration_analysis(df):
    avg_duration = round(df['duration_min'].mean(), 2)
    top10_avg = round(df[df['position'] <= 10]['duration_min'].mean(), 2)
    bottom40_avg = round(df[df['position'] > 10]['duration_min'].mean(), 2)
    return avg_duration, top10_avg, bottom40_avg

def unique_artist_count(df):
    return df['artist'].nunique()