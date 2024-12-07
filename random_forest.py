import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix

#Load data
data_path = "data/spy_data_cleaned.py"
df = pd.read_csv(data_path)

#Target creation
df["target"] = (df["Close"] > df["Open"]).astype(int) # close is higher than open meaning profit

# Drop rows with missing values
df.dropna(inplace=True)
