import configparser
import requests

class HKBU_ChatGPT():
    def __init__(self, token):
        self.token = token
    '''
    def __init__(self,config_='./config.ini'):
        if type(config_) == str:
            self.config = configparser.ConfigParser()
            self.config.read(config_)
        elif type(config_) == configparser.ConfigParser:
            self.config = config_
    '''
    def submit(self,message):
        try:
            conversation = [{"role": "user", "content": message}]
            '''
            url = (f"{self.config['CHATGPT']['BASICURL']}/deployments/"
                    f"{self.config['CHATGPT']['MODELNAME']}/chat/completions/"
                    f"?api-version={self.config['CHATGPT']['APIVERSION']}")
            '''
            url = (f"https://chatgpt.hkbu.edu.hk/general/rest/deployments/"
                    f"gpt-35-turbo-16k/chat/completions/"
                    f"?api-version=2023-12-01-preview")

            headers = { 'Content-Type': 'application/json', 'api-key': self.token }
            payload = { 'messages': conversation }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                return 'Error:'+str(response)
        except:
            return 'Error in HKBUGPT'

if __name__ == '__main__':
    ChatGPT_test = HKBU_ChatGPT(token)

    while True:

        user_input = input("Typing anything to ChatGPT:\t")
        response = ChatGPT_test.submit(user_input)
        print(response)
