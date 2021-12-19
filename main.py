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
    comment = session.get_project(id).get_comments()[0]

    user = html.unescape(comment.author)
    userID = str(comment.author_id)
    comment = html.unescape(comment.content)

    return [comment, user, userID]

def getFollowers() :
    followers = []

    for user in session.get_user(username).get_followers(all=True) :
        followers.append(str(user.id))
    
    return followers

def main() :
    print("Starting..")

    with open("banlist.txt", "r") as f :
        banlist = f.read().split("\n")

    lastComment = []
    while True :
        try :
            try :
                latestComment = getLatestComment(commentSourceProject)
            except IndexError :
                print("No comments!")
                connection.set_cloud_variable("comment", int(encodeString("Either my code broke, or there aren't any comments.")))
                connection.set_cloud_variable("username", int(encodeString("Nobody")))

            if not lastComment == latestComment :
                print("New comment by %s!" % (latestComment[1]))
                lastComment = latestComment
                print(lastComment)

                if latestComment[1].lower() in banlist or latestComment[2].lower() in banlist :
                    print("The user is banned!")
                    connection.set_cloud_variable("comment", int(encodeString("The author of this comment has been banned.")))
                    connection.set_cloud_variable("username", int(encodeString("INFO")))
                else :
                    followers = getFollowers()
                    #print(followers)

                    special = latestComment[2] in followers
                    print(["This user is not a follower", "This user is a follower!"][int(special)])

                    connection.set_cloud_variable("comment", int(encodeString(latestComment[0])))
                    connection.set_cloud_variable("username", int(encodeString(latestComment[1])))
                    connection.set_cloud_variable("special", int(special))
        except Exception as e :
            print(e)
        
        time.sleep(checkingInterval)

if __name__ == "__main__" :
    main()