

#import pync
import feature_extraction as fe
import pandas as pd
import pync
import pickle as pkl

#load the model
model = pkl.load(open('/Users/raresnitu/Documents/security_project/ELEC0138_Project/phishing_attack/model_MLP.pkl', 'rb'))

#input the URL
url = input("Enter the URL: ")

#extract the features
features = fe.extract_features(url)
feature_list = features["features"]

feature_list = [item for sublist in feature_list for item in sublist]

#predict the URL
prediction = model.predict([feature_list])

#show the result on the terminal and notify the user

if prediction == 1:
    print("This is a phishing website")
    pync.notify("This is a phishing website", title="Phishing Attack",sender='com.apple.Terminal')
elif prediction == 0:
    print("This is a legitimate website")
    pync.notify("This is a legitimate website", title="Phishing Attack",sender='com.apple.Terminal')
else:
    print("Error: This site is not working")
    pync.notify("Error: This site is not working", title="Phishing Attack",sender='com.apple.Terminal')




