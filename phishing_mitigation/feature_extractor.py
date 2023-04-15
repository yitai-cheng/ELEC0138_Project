import re
import requests
import tldextract
import pickle as pkl
from bs4 import BeautifulSoup
from sklearn.preprocessing import StandardScaler
#load X_train as dataframe
X_train = pkl.load(open('/Users/raresnitu/Documents/security_project/ELEC0138_Project/phishing_mitigation/X_train.pkl', 'rb'))

def extract_features(url):

    #intialise feature list:
    features = []

    # Extract the domain name and path from the URL
    #domain name
    domain_name = re.findall(r'://([^/]+)', url)[0]
    path = re.findall(r'[^/]+(/.*)?', url)
    path = path[0] if path else ""

    #Length of the URL

    url_length = len(url)
    features.append(url_length)
    
    #Length of hostname

    hostname_length = len(domain_name)
    features.append(hostname_length)

    #Whether the hostname is an IP address

    if re.match(r'\d+\.\d+\.\d+\.\d+', domain_name):
        ip = 1
    else:
        ip = 0
    features.append(ip)

    #Number of dots in the URL

    dots = url.count('.')
    features.append(dots)

    #Number of question marks in the URL

    question_marks = url.count('?')
    features.append(question_marks)

    #Number of equals signs in the URL

    equals = url.count('=')
    features.append(equals)

    #Number of slashes in the URL

    slashes = url.count('/')
    features.append(slashes)

    #Ratio of digits to letters in the URL

    digits = sum(c.isdigit() for c in url)
    features.append(digits/len(url))

    #Ration of digits to letters in the hostname

    digits = sum(c.isdigit() for c in domain_name)
    features.append(digits/len(domain_name))

    #If the top level domain is in the subdomain

    tld = tldextract.extract(url).suffix
    subdomain = domain_name[:-len(tld) - 1]
    if tld in subdomain:
        tld_in_subdomain = 1
    else:
        tld_in_subdomain = 0
    features.append(tld_in_subdomain)

    #If hostname has a prefix or suffix

    if re.match(r'www\.|\.com$', domain_name):
        prefix = 1
    else:
        prefix = 0
    features.append(prefix)
    
    #lenght of the shortest word in the hostname

    shortest_word = min(len(word) for word in domain_name.split('.'))
    features.append(shortest_word)

    #lenght of the longest word in URL

    word_URL = re.findall(r'[a-zA-Z]+', url)
    length_word_URL = max(len(word) for word in word_URL)
    features.append(length_word_URL)

    #Lenght of the longest word in path

    word_path = re.findall(r'[a-zA-Z]+', path)
    if  word_path:
        length_word_path = max(len(word) for word in word_path)
    else:
        length_word_path = 0
    features.append(length_word_path)

    #if contains phishing hints

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Cannot establish a connection to the website. Error: {e}"
        }
    soup = BeautifulSoup(response.text, 'html.parser')
    phishing_hints_list = ['phishing', 'login', 'account', 'signin', 'secure', 'confirm', 'verification', 'security', 'banking', 'bank', 'challenge', 'challeng','password','update','verify']
    phishing_hints = any(word in soup.text for word in phishing_hints_list)
    if phishing_hints:
        phishing_hints_true = 1
    else:
        phishing_hints_true = 0
    features.append(phishing_hints_true)

    #if there are empty title tags

    title = soup.find('title')
    if not title or not title.text.strip():
        empty_title_tag = 1
    else:
        empty_title_tag = 0
    features.append(empty_title_tag)

    #weathere thr domain name is in the title tag

    title = soup.find('title')
    if title and domain_name in title.text:
        domain_in_title = 1
    else:
        domain_in_title = 0
    features.append(domain_in_title)

    #if the url has a google index
   
    google_index = re.findall(r'google.com/search', url)
    if google_index:
        google_index_true = 1
    else:
        google_index_true = 0
    features.append(google_index_true)

    scaler = StandardScaler()
    scaler.fit(X_train)
    features = scaler.transform([features])
    features = features.tolist()
    
    return {
        "success": True,
        "features": features
    }

