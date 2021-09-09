import webbrowser
from random import randint
import urllib.request
from bs4 import BeautifulSoup

link = webbrowser.get()

catNature = ["theplanetd", "bestplaces_togo",  "chrisburkard", "giuliogroebert", "wildernesstones", "tom_juenemann", 
"withluke", "joelsartore", "brianskerry", "alaskanps", "montereybayaquarium", "nationalparkservice", "dailyoverview", 
"rainforestalliance", "nature_org", "wanderireland", "amivitale"]

catDog = ["puppyearth", "dog", "tuckerbudzyn", "dogs.media", "thedogist", "weratedogs", "dogsofinstagram",
"just.love.dogs", "puppies.club", "yourdogsinsta", "cutestpuppiesforyou",
"puppy_lovings", "barked", "charlie_the_golden18",
"coconutricebear", "marleyandmeinnyc", "dunkinandfriends", "milperthusky", "lnstahusky", "loki", 
"dogsthathike", "campingwithdogs", "rastawhiteshepherd", "whiteswissgram", "halfhuskybros","fullhdog"]

catTravel = ["earthpix", "loic.lagarde", "beautifuldestinations", "doyoutravel", "gypsea_lust", "itsbeautifulhere", 
"wearetravelgirls", "kellyalack", "annstreetstudio", "taramilktea", "muradosmann", "jackharding", "lucylaucht",
"finduslost", "prettylittlelondon", "calsnape", "wonderful_places", "theprettycities", "polabur", "theslowtraveler"]

def url(str):
    index = str.find("shortcode")
    url = str[index+12:index+23]
    return("https://www.instagram.com/p/" + url + "/")


def accFollowers(str):
    index = str.find("userInteractionCount")
    accFollows = str[index+23:index+48]
    static = accFollows.find("}")
    numFollows = str[index+23:index+23+static-1]
    return(numFollows)

def postLikes(str):
    index = str.find("edge_media_preview_like")
    numLikes = str[index+34:index+48]
    static = numLikes.find("}")
    totalLikes = str[index+34:index+34+static]
    return(totalLikes)

def postComments(str):
    index = str.find("edge_media_to_comment")
    srchComments = str[index+32:index+48]
    static = srchComments.find("}")
    numComments = str[index+32:index+32+static]
    return(numComments)

def searchCat(cat):
    print("Scrubbing Data. . .")
    for i in range(len(cat)):
        listUrl = []
        listLikes = []
        listComments = []
        listCaption = []
        wp = "https://www.instagram.com/" + cat[i] + "/"
        ws = urllib.request.urlopen(wp)
        scrape = BeautifulSoup(ws.read(), "html.parser")
        sourceString = str(scrape)
        numFollows = accFollowers(sourceString)
        keepG = 0
        keepGoing = True
        numG = 0
        while keepGoing == True:
            keepG = keepG + 1
            index = sourceString.find("__typename")
            if index == -1:
                keepGoing = False
            else:
                keepGoing = True
            sourceString2 = ""
            end = (len(sourceString))
            sourceString2 = sourceString[index+1:end]
            sourceString = sourceString2
            listUrl.append(url(sourceString))
            listLikes.append(postLikes(sourceString))
            listComments.append(postComments(sourceString))
            listCaption.append(postCaption(sourceString))
            numG+= 1
        print("----------------")
        print("Posts From: " + wp)
        print("Followers : " + str(numFollows))
        print("Top Three Posts: " + cat[i])
        for o in range(len(listUrl)):
            #loc = o
            for i in range(len(listUrl)-o):
                if int(listLikes[o]) < int(listLikes[i+o]):
                    temp = listLikes[o]
                    listLikes[o] = listLikes[i+o]
                    listLikes[i+o] = temp

                    temp = listComments[o]
                    listComments[o] = listComments[i+o]
                    listComments[i+o] = temp

                    temp = listUrl[o]
                    listUrl[o] = listUrl[i+o]
                    listUrl[i+o] = temp

                    temp = listCaption[o]
                    listCaption[o] = listCaption[i+o]
                    listCaption[i+o] = temp
        total = 0
        for i in range(len(listLikes)):
            total += int(listLikes[i])
        avgPer = total/len(listLikes)
        avgPer = int(avgPer)
        for l in range(3):
            print(listUrl[l])
            print("Likes: " + str(listLikes[l]) + " (" + str(round((int(listLikes[l])/avgPer) * 100)) + "% Better than average post)")
            print("Comments: " + listComments[l])
            print("Caption: ")
            print(listCaption[l])
            print()
            if l == 0:
                link.open_new_tab(listUrl[l]) 

def postCaption(str):
    index = str.find("edge_media_to_caption")
    pCaption = str[index+50:index+2000]
    static = pCaption.find("}]}")
    postCaptions = str[index+50:index+50+static-2]
    pstCaption = refineCaptions(postCaptions)
    return(pstCaption)

def refineCaptions(str):
    pstCaption = str
    pstCaption = pstCaption.replace("\\n", "\n")
    pstCaption = pstCaption.replace("\\u201c", "\"")
    pstCaption = pstCaption.replace("\\u201d", "\"")
    pstCaption = pstCaption.replace("\\u2019", "\'")
    pstCaption = pstCaption.replace("\\ud83d\\ude02", "[emoji]")
    return(pstCaption)

def chooseCat():
    print("These are the available categories to search through: travel, dog, and nature.")
    print("You will have to retype your chosen category to confirm!")
    chosenCat = input("Howdy brother, what category can we search for ya today? Input: ")
    return chosenCat