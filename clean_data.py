import os
import numpy as np
import pandas as pd

# --- User-changeable parameters ---
csv_path = "16P.csv"   
index_col = 0                # column index for the run-number 
num_question_cols = 60       # number of question columns 
mbti_col_index = 61          # zero-based index (62nd column) for MBTI label in original description
samples_per_type = 225       # number of respondents to sample per MBTI type
output_path = "mbti_base_profiles.csv"
random_seed = 42
# ----------------------------------

np.random.seed(random_seed)

# Standard 16 MBTI types 
mbti_types = [
    "INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"
]

def prepare_df_from_csv(path):
    if os.path.exists(path):
        print(f"Reading CSV from: {path}")
        df = pd.read_csv(csv_path, header=0, encoding='latin1')
        print("CSV loaded. Shape:", df.shape)
        return df
    else:
        print(f"CSV not found at {path}.")

# Load or simulate dataset
df = prepare_df_from_csv(csv_path)

# set MBTI column name, and feature columns
mbti_col_name = "Personality"
all_cols = list(df.columns)
index_col = "Response Id"
feature_cols = [c for c in df.columns if c not in (index_col, mbti_col_name)]


print(f"Detected MBTI column: '{mbti_col_name}'")
print(f"Number of feature columns used: {len(feature_cols)}")

# Ensure feature columns are numeric
df_features = df[feature_cols].apply(pd.to_numeric, errors='coerce')
df[feature_cols] = df_features

# Create base profiles for each MBTI type
base_profiles = []

for mb in mbti_types:
    df_mb = df[df[mbti_col_name] == mb]
    sampled = df_mb.sample(n=samples_per_type, replace=False, random_state=random_seed)    # sampled features shape: (samples_per_type, num_question_cols)
    features = sampled[feature_cols].to_numpy(dtype=float)  # shape (64,60)

    # transpose to (60,64) where each row is a channel for one question across 64 respondents
    channels = features.T  # shape (60,64)

    # For each channel (length 64), reshape to (8,8) using column-major order (Fortran order)
    channel_matrices = np.stack([row.reshape((15,15), order='F') for row in channels], axis=0)  # shape (60,8,8)

    # Average pooling: mean across spatial dims (8x8) -> scalar per channel
    pooled = channel_matrices.mean(axis=(1,2))  # shape (60,)

    # reshape to (60,1,1) then to (60,1) as requested
    pooled_3d = pooled.reshape((num_question_cols,1,1))
    pooled_2d = pooled.reshape((num_question_cols,1))

    # We'll store flattened 60-vector (pooled) as base profile
    base_profiles.append([mb] + pooled.tolist())

# Create DataFrame for base profiles
cols_out = ["MBTI"] + [f"Q{i+1}" for i in range(num_question_cols)]
base_df = pd.DataFrame(base_profiles, columns=cols_out)

# Save to CSV
base_df.to_csv(output_path, index=False)
print(f"\nSaved base profiles CSV to: {output_path}")


# Display the resulting DataFrame to the user in a table view
try:
    from caas_jupyter_tools import display_dataframe_to_user
    display_dataframe_to_user("MBTI Base Profiles", base_df)
except Exception:
    # fallback: print head
    print("\nBase profiles (preview):")
    print(base_df.head())

# Provide path to output
print(f"\nOutput file path: {output_path}")

