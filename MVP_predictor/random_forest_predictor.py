import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics


df = pd.read_csv('player_data_mvp.csv')

df = df[["G","MP","FG","FGA","FG%","3P","3PA","3P%","FT","FTA","FT%","ORB","DRB","AST","STL","BLK","TOV","PTS","MVP"]]
df = pd.get_dummies(df)
df2 = df.copy()


labels = np.array(df['MVP'])
df = df.drop('MVP', axis=1)
feature_list = list(df.columns)

# Convert to numpy array
df = np.array(df)
df = np.nan_to_num(df)

train_features, test_features, train_labels, test_labels = train_test_split(df, labels, test_size = 0.25, random_state = 41)
print(test_labels)
rf = RandomForestClassifier(n_estimators = 1000, random_state = 41)
# Train the model on training data
rf.fit(train_features, train_labels)

predictions = rf.predict(test_features)
print("Accuracy", metrics.accuracy_score(test_labels, predictions))


importances = list(rf.feature_importances_)
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];


print("MVP Predictions")
#["G","MP","FG","FGA","FG%","3P","3PA","3P%","FT","FTA","FT%","ORB","DRB",,"AST","STL","BLK","TOV","PTS","MVP"]
#TODO integrate with NBA API
Giannis = [[82,1354*2,802,691*2,.580,32,94*2,.170,264*2,377*2,0.7,96*2,417*2, 245*2, 56*2, 61*2, 162*2,1082*2]]
Harden = [[82,1530*2,840,958*2,.438,199*2,531*2,0.375,411*2,475*2,0.865,32*2,228*2,350*2,83*2,26*2,228*2,1450*2]]
print(rf.predict(Giannis))
print(rf.predict_proba(Giannis))

print(rf.predict(Harden))
print(rf.predict_proba(Harden))
