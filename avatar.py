from io import BytesIO
from PIL import Image
import requests
import os
import time

def createDirectory(user):
    os.system("mkdir " + os.path.join(f"C:{os.sep}", "Users", os.environ['USERNAME'], "Desktop", f"{user.lower()}-followers-avatares"))
    
def getFollowersAvatares(userFollowers, user):

    req = requests.get(userFollowers, timeout=30) # Throws Timeout Error if the waiting time pass of 30

    req.raise_for_status()

    userFollowersData = req.json() # Return a list with followers info

    for userFollowerData in userFollowersData:

        req_avatar = requests.get(userFollowerData['avatar_url'], timeout=30)

        req.raise_for_status()

        avatar_image = Image.open(BytesIO(req_avatar.content)) # Response.content returns body's page encoding to byte
        # BytesIO decodes to string

        avatar_image.save(os.path.join(f"C:{os.sep}", "Users", os.environ['USERNAME'], "Desktop", f"{user.lower()}-followers-avatares", f"{userFollowerData['login']}.png"))

def getUser(user):

    req = requests.get(f"https://api.github.com/users/{user}", timeout=30, allow_redirects=True)

    req.raise_for_status() # Verify if status code isn't 404. If it is, it throws a HTTP Error

    userData = req.json() # Decodes json to dict

    createDirectory(user)

    getFollowersAvatares(userData['followers_url'], user)

if __name__ == "__main__":

    try:
        start_time = time.time() # Starts before request
        getUser(input("Digite o seu nome de usuário do github: "))
    except requests.exceptions.HTTPError as error:
        if error.args[0][0:3] == "404": # If status code of response is 404, perhaps the server resource wasn't found because the username was digited in wrong manner
            print("Erro 404! Talvez você tenha digitado um nome de usuário inválido!")
            getUser(input("Digite o seu nome de usuário do github: "))
        else:
            print(error)
    except requests.exceptions.ConnectionError:
        print("Houve um erro de conexão!")
    except requests.exceptions.Timeout:
        end_time = time.time()
        print(f"O tempo de conexão foi expirado! Sua solicitação durou {end_time - start_time} milissegundos! Por favor, tente novamente!")
    except requests.exceptions.RequestException:
        print("Houve um erro em sua solicitação!")



        
    
