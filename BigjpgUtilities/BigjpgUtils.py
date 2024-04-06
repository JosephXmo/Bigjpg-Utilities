import requests
import json

apiKey = ''

def setAPIKey(keyArg):
    global apiKey
    apiKey = keyArg

def printAPIKey():
    print(apiKey)

def initializeEnlargeTask(style, noise, x2, urlMode, filePath):
    if apiKey == '':
        print("Attention: You might not set API key yet. Without an API key, you cannot establish a enlarge task.")

    # a / p
    if style == 'a':
        style = 'art'
    elif style == 'p':
        style = 'photo'
    else:
        style = ''

    # n -> l -> m -> h -> vh
    if noise == 'n':
        noise = '-1'
    elif noise == 'l':
        noise = '0'
    elif noise == 'm':
        noise = '1'
    elif noise == 'h':
        noise = '2'
    elif noise == 'vh':
        noise = '3'
    else:
        noise = ''

    x2 = int(x2 / 2)

    file_name = filePath.split('/')[-1]
    
    input = filePath

    data = {
        'style': style,
        'noise': noise,
        'x2': str(x2),
        'file_name': file_name,
        'input': input
    }

    return data

def enlargeImage(task):
    if apiKey == '':
        print("Error: Please set API key before submitting any enlargement task!")
        return ''

    enlargeSession = requests.post(
        url = 'https://www.bigjpg.com/api/task/',
        headers = {'X-API-KEY': apiKey},
        data = json.dumps(task)
    )
    tid = dict(enlargeSession.json()).get('tid')
    return tid

def queryEnlargeSession(tid):
    enlargeSession = requests.get(url = 'https://www.bigjpg.com/api/task/' + tid)
    return dict(enlargeSession.json()).get(tid)

def retryEnlargeSession(tid):
    retrySession = requests.post(url = 'https://www.bigjpg.com/api/task/' + tid)
    if dict(retrySession.json()).get('status') == 'ok':
        return session
    else:
        return dict(retrySession.json()).get(tid)

def printSession(tid):
    session = dict(queryEnlargeSession(tid))

    print("*** Task " + tid + " ***")
    if 'status' in dict(session).keys():
        if dict(session).get('status') == 'failed':
            print("Status: Failed. Detail: " + dict(session).get('status'))
        elif dict(session).get('status') == 'new':
            print("Status: Enlarge in progress, please wait...")
        elif dict(session).get('status') == 'success':
            print("Status: Success, " + str(int(dict(session).get('size')) / 1000) + " KB in total.\nDownload URL: " + dict(session).get('url'))
        else:
            print("Unknown status \"" + session.get('status') + "\" received. Please submit raw data to developer for further help.")
            print("Raw data received: ")
            print(json.dumps(session, indent=4))
    else:
        print("Enlarge session submitted.\nAPI calls left: " + str(dict(session).get('remaining_api_calls')) +
              ', Minutes left: ' + str(dict(session).get('minute')))
