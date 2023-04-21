#program that test if the website is phishing or not and notifies the user

import feature_extractor as fe
import pickle
import pync

#load the model
model = pickle.load(open('//Users/raresnitu/Documents/security_project/ELEC0138_Project/phishing_mitigation/model_MLP.pkl', 'rb'))

#Get the URL

url = input("Enter the URL: ")

#Extract the features

features = fe.extract_features(url)
feature_list = features['features']


feature_list = [values for sublist in feature_list for values in sublist]

print(feature_list)

#Predict the url

prediction = model.predict([feature_list])

#show the result

if prediction == 1:
    print("Phishing website")
    pync.notify("Phishing website", title="Phishing website",sender="com.apple.Terminal")
elif prediction == 0:
    print("Not a phishing website")
    pync.notify("Not a phishing website", title="Not a phishing website",sender="com.apple.Terminal")
else:
    print("Error")
