from Tix import _dummyComboBox

name = raw_input("Enter User Name:")


import requests


BASE_URL = "https://api.instagram.com/v1"
APP_ACCESS_TOKEN = "398715021.1c98adf.13e3472fd0914d20bcccb1bd9f89a038"
response = ""

# To print self info.
def my_info():
    URL = BASE_URL + "/users/self?access_token=%s" %(APP_ACCESS_TOKEN)
    response = requests.get(URL)
    return response.json()


# To print User's id.
def get_user_id(name):
    URL = BASE_URL + "/users/search?q=%s&access_token=%s" %(name,APP_ACCESS_TOKEN)
    response = requests.get(URL)
    info = response.json()['data']
    if len(info)>0:
        user_id = response.json()['data'][0]['id']
        return user_id
    # If no user with the required name is found, the code should end at that point.

    else:
        print "No User Found!!!"
        exit()


# To print User's posts.
def get_user_media(name):
    user_id = get_user_id(name)
    URL = BASE_URL +"/users/%s/media/recent?access_token=%s" %(user_id,APP_ACCESS_TOKEN)
    response = requests.get(URL)
    info = response.json()["data"]
    if info:
        for i in range(len(info)):
            print "S. No.   :     %d" % (i+1)
            print "User ID:       %s" %(info[i]['caption']['from']['id'])
            print "User Name     :%s"   %(info[i]['caption']['from']['username'])
            print "Post ID:       %s" % (info[i]['id'])
            print "post Link:     %s" % (info[i]["link"])
            print "Comment Count: %s" % (info[i]["comments"]["count"])
            print "Like Count :   %s" % (info[i]["likes"]['count'])
            if info[i]["caption"]['text']:
                print "Caption:    %s" % (info[i]["caption"]['text'])
            else:
                print "Sorry!!! No caption"

    else:
        print "Sorry!! The User has no Posts"
    action(name)


# Function to fetch a particular Media Id
def get_media_id(name):
    serial_number = int(raw_input("Enter the serial number of the post!!"))
    user_id = get_user_id(name)
    URL = BASE_URL + "/users/%s/media/recent?access_token=%s" % (user_id, APP_ACCESS_TOKEN)
    media_id = []
    response = requests.get(URL).json()
    info = response['data']
    for i in range(len(info)):
        media_id.append(info[i]['id'])
    return media_id[serial_number-1]


# Function to like the post of the user that has been entered and Post order.
def like_a_post(name):
    media_id = get_media_id(name)
    URL = BASE_URL + "/media/%s/likes" %(media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    response = requests.post(URL,payload).json()
    if response['meta']['code'] == 200:
        print "Congratulations! The post has been successfully liked"
    else :
        print "OOPS!! Have a look at your code"

    action(name)


# Function to comment on the post.
def comment_on_a_post(name):
    media_id = get_media_id(name)
    text = raw_input("Enter the comment")
    URL = BASE_URL + "/media/%s/comments" % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN,"text":text}
    response = requests.post(URL , payload).json()
    print response
    if response["meta"]["code"]==200:
        print "Successfully commented!!"
    else :
        print 'Could not comment!!!, Recheck your comment'
        print response['meta']["error_message"]
    action(name)


 # Function to return the comment id of a comment through a Search Hit.
def get_comment_id(name):
    media_id = get_media_id(name)
    URL = BASE_URL + "/media/%s/comments?access_token=%s" %(media_id,APP_ACCESS_TOKEN)
    word = raw_input("Enter the word you are searching for")
    response = requests.get(URL)
    info = response.json()["data"]
    comment_id = []

#Storing all the comment_ids of comments containing word entered by user in a list "comment_id)
    for i in range(len(info)):
        split = info[i]['text'].split()
        if word in split:
            comment_id.append(info[i]['id'])
#Storing media_id as last element of 'comment_id' so that we dont have to call media_id again while deleting the comment
    comment_id.append(media_id)
    if len(comment_id)>0:
        return comment_id
    else:
        print "No Comment Found!!!"
    action(name)



# Function to print the name of the User commented along with the comments.
def print_all_comments(name):

    media_id = get_media_id(name)
    URL = BASE_URL + "/media/%s/comments?access_token=%s" % (media_id, APP_ACCESS_TOKEN)
    response = requests.get(URL)
    info = response.json()["data"]
    if len(info)==0:
        print "Sorry!!! No Comments!!"
        return None
    for i in range(len(info)):
        print "%s commented %s" % (info[i]["from"]["username"], info[i]['text'])
    action(name)



# Deleting all the comments containing particular word by help of the list of comment_id returned by the get_comment_id() function
def delete_comment(name):
    comment_id = get_comment_id(name)
#in get_comment_id, media_id was stored as last element
    media_id = comment_id[len(comment_id)-1]
    if len(comment_id)>0:
#deleting all the comments containing particular word by help of the list of comment_id returned by the get_comment_id() function
        for i in range(len(comment_id)-1):    #the last entry is media_id, While previous ones are comment_id.., so we are accessing the elements before the last elements..
            URL = BASE_URL + "/media/%s/comments/%s?access_token=%s" %(media_id,comment_id[i],APP_ACCESS_TOKEN)
            print URL
            response = requests.delete(URL)
            if response.status_code == 200:
                print  "Successfully Deleted!!!"
            else :
                print "Could Not Delete!! Sorry!!"
    else :
        print "No Such Comment Found!!!!"
    action(name)

# Function to return the average number of words in a comment.
def average_number_of_words_in_comment(name):
    media_id = get_media_id(name)
    URL = BASE_URL + "/media/%s/comments?access_token=%s" % (media_id, APP_ACCESS_TOKEN)
    response = requests.get(URL)
    sum = 0
    info = response.json()["data"]
    number_of_entries = len(info)
    for i in range(number_of_entries):
        split = info[i]['text'].split()
        number_of_words = len(split)
        sum += number_of_words
    if sum>0:
        average = float(sum/number_of_entries)
        print average
    else :
        avg = 0
        print avg


# Function to get the comment_id of all the comments present in the entered given media.
def get_all_comments(name):
    media_id = get_media_id(name)
    URL = BASE_URL + "/media/%s/comments?access_token=%s" % (media_id, APP_ACCESS_TOKEN)
    response = requests.get(URL)
    info = response.json()["data"]
    comment_id = []
    for i in range(len(info)):
        comment_id.append(info[i]['id'])
    comment_id.append(media_id)
    return  comment_id

 #An extra function, Not in objectives to delete alll the comments at once
def delete_all_comments(name):
    comment_id = get_all_comments(name)
    # in get_comment_id, media_id was stored as last element
    media_id = comment_id[len(comment_id) - 1]
    if len(comment_id) > 0:
        for i in range(len(comment_id) - 1):  # the last entry is media_id, While previous ones are comment_id.., so we are accessing the elements before the last elements..
            URL = BASE_URL + "/media/%s/comments/%s?access_token=%s" % (media_id, comment_id[i], APP_ACCESS_TOKEN)
            print URL
            response = requests.delete(URL)
            if response.status_code == 200:
                print  "Successfully Deleted!!!"
            else:
                print "Could Not Delete!! Sorry!!"
    else:
        print "No Such Comment Found!!"
    action(name)



#Asks user to choose actions from the set of available actions...
def action(name):
    print "Like                   :1"
    print "Comment                :2"
    print "Delete Comment         :3"
    print "Print all comments     :4"
    print "My Information         :5"
    print "Average N0 of words in comment :6"
    print "Delete All coomments   :7"
    print "Exit                   :0"
    actions = int(raw_input("Choose Action : "))
    if actions == 1:
       print like_a_post(name)
    elif actions == 2:
        comment_on_a_post(name)
    elif actions == 3:
        delete_comment(name)
    elif actions == 4 :
        print_all_comments(name)
    elif actions == 5:
       print my_info()
    elif actions==6:
        average_number_of_words_in_comment(name)
    elif actions == 7:
        delete_all_comments(name)
    elif actions == 0:
        exit()
    else :
        print "Invalid Entry!!"


get_user_media(name)
action(name)
