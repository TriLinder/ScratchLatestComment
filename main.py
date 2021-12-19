from scratchclient import ScratchSession
import html
import time

alphabet = "0123456789abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

commentSourceProject = 618979491
cloudProject = 618979491
checkingInterval = 60

username = "SimpleFun"

with open("password.pswd", "r") as f :
    pswd = f.read()

session = ScratchSession(username, pswd)
connection = session.create_cloud_connection(cloudProject)

def encodeString(string) :
    encoded = "10"

    for char in string :
        if char in alphabet :
            encoded = encoded + str('{:02d}'.format(alphabet.find(char)))
        else :
            encoded = encoded + str('{:02d}'.format(alphabet.find("?")))
        
    return encoded

def getLatestComment(id) :
    user = html.unescape(session.get_project(id).get_comments()[0].author)
    comment = html.unescape(session.get_project(id).get_comments()[0].content)

    return [comment, user]

def main() :
    print("Starting..")

    with open("banlist.txt", "r") as f :
        banlist = f.read().split("\n")

    lastComment = []
    while True :
        try :
            latestComment = getLatestComment(commentSourceProject)

            if not lastComment == latestComment :
                print("New comment by %s!" % (latestComment[1]))
                lastComment = latestComment
                print(lastComment)

                if latestComment[1].lower() in banlist :
                    print("The user is banned!")
                    connection.set_cloud_variable("comment", int(encodeString("The author of this comment has been banned.")))
                    connection.set_cloud_variable("username", int(encodeString("INFO")))
                else :
                    connection.set_cloud_variable("comment", int(encodeString(latestComment[0])))
                    connection.set_cloud_variable("username", int(encodeString(latestComment[1])))
        except Exception as e :
            print(e)
        
        time.sleep(checkingInterval)

if __name__ == "__main__" :
    main()