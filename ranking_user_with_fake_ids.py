import tweepy
from pprint import pprint
from datetime import timedelta
import datetime,time,os,glob,math,sys,csv

#This is version 3

#API Info
BEARER_TOKEN = "This is the token."
CONAUMER_KEY = "This is the key."
CONAUMER_SECRET = "This is the cunsumer key."
ACCESS_TOKEN = "This is the access token."
ACCESS_TOKEN_SECRET = "This is the access token secret."

#create cliant info
def ClientInfo():
    client = tweepy.Client(
    bearer_token = BEARER_TOKEN,
    consumer_key = CONAUMER_KEY,
    consumer_secret = CONAUMER_SECRET,
    access_token = ACCESS_TOKEN,
    access_token_secret = ACCESS_TOKEN_SECRET 
    )
    return client

def GetAuth():
    auth = tweepy.OAuthHandler(CONAUMER_KEY, CONAUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit = True)
    return api

def ClearTextFile(text_name):
    #print (text_name)
    if text_name.find(".csv") == -1 :
        if text_name.find(".txt") == -1 :
            if text_name.find("ranking_user/")  == -1 :
                str_a = 'ranking_user/'+text_name+'.txt'
            else :
                str_a = text_name+'.txt'
        else :
            if text_name.find("ranking_user/")  == -1 :
                str_a = 'ranking_user/'+text_name
            else :
                str_a = text_name
    else:
        if text_name.find("ranking_user/")  == -1 :
            str_a = 'ranking_user/'+text_name
        else:
            str_a = text_name
    
    #print (str_a)
    if text_name != None:
        with open(str_a,'w',encoding='UTF-8') as fp:
            fp.close()
    return 0


#Get User Info from User Name
def GetUserFromUserName():

    user_name = 'YoheiKoike'
    
    user = ClientInfo().get_user(username=user_name)
    #pprint (user)
    
    return user


def WriteTweetIdToText(tweets):
    str_a = "aaa"
    ClearTextFile(text_name='tweet_ids')
    with open('ranking_user/tweet_ids.txt','a',encoding='UTF-8') as fp:
        i = 1
        for tweet in tweets :
            #str_a is "num,tweet_id"
            str_a= str(i)+','+str(tweet[0])+','+str(tweet[-1])
            print(str_a,file=fp)
            i+=1
    fp.close()
    return 0


def GetTweet_v02(user,maxnum):
    results = []
    
    api = GetAuth()
    
    #pprint (user.data.id)
    tweets = tweepy.Cursor(api.user_timeline,user_id=user.data.id).items(maxnum)
    num = 1
    
    with open('ranking_user/all_tweet.txt','a',encoding='UTF-8') as fp:
        for tweet in tweets :
            tweet.created_at += timedelta(hours=9)
            results.append([tweet.created_at,tweet.text,tweet.id])
            
            #write all tweets to all_tweet.txt file
            print("\n[",num,"]",file=fp)
            pprint (results[num-1],stream=fp)
            print("\n\n",file=fp)
            num+=1
    
        fp.close()
    
    return results

def Ranking_LikingUsers(user_ranking, users):
    flag = int(0)
    i = int(0)
    with open('ranking_user/log_test2.txt','a',encoding='UTF-8') as fp:
        for user in users:
            #print (user[0])
            flag = int(0)
            i = int(0)
            for i in range(len(user_ranking)):
                #print(type(user_ranking[i][0]))
                #print(type(user[0]))
                if flag == int(1):
                    flag = 1
                elif (user_ranking[i][0]) == (user[0]) :
                    print ("i = ",i,file=fp)
                    print(user_ranking[i][0],"==",user[0],file=fp)
                    print(user_ranking[i][1],"==",user[1],file=fp)
                    user_ranking[i][3] += 1
                    print ("count is ", user_ranking[i][3],file=fp)
                    flag = 1
            if flag == int(0):
                user.append(int(1))
                user[3] = 1
                print("\nThis is first user",file=fp)
                print (user,file=fp)
                user_ranking.append(user)
                
                
                
                #print (user)
        print ("\n\n 終わり\n\n\n ",file=fp)
    fp.close()
    
    
    return user_ranking


def sortRank(counted_users):
    
    temp_a = [[0,"TestTarou","Tarou",0]]
    #pprint(counted_users)
    for user in counted_users :
        #pprint (user)
        for i in range(len(temp_a)):
            if int(user[3]) >= int(temp_a[i][3]):
                temp_a.insert(i,user)
                break
                #pprint(user)
            elif int(user[3]) < int(temp_a[i][3]):
                if i == ( len(temp_a) - 1):
                    temp_a.append(user)
                    break
                    #pprint(user)
    if temp_a[-1][3]==0 :
        #print ("\n\n",temp_a[-1],"\n\n")
        del temp_a[-1]
    return temp_a


def CutStrOutList(tmp_str):
    tmp_list = []
    tmp_str = tmp_str.split('\n')
    tmp_list = tmp_str[0].split(',')
    return tmp_list

def TakeDateDeleteTime(tmp_list):
    date = []
    date = tmp_list[1].split(' ',2)
    date = date[0].split('-')
    return date

def CollectTweetIdsByTime(start_date,end_date):
    #Collect Ids during the time
    
    results = []
    
    #read the data
    with open('ranking_user/tweet_ids.txt','r') as fp:
        for tmp_str in fp:
            #pprint (tmp_str)
            tmp_list = CutStrOutList(tmp_str)
            
            #pprint (tmp_list)
            tmp_date = TakeDateDeleteTime(tmp_list)
            
            #print (tmp_date)
            
            this_date = datetime.datetime(int(tmp_date[0]),int(tmp_date[1]),int(tmp_date[2]))
            if start_date <= this_date and this_date <= end_date :
                #print ("Good")
                #print(this_date)
                results.append(tmp_list[2])
                    
            
        
        
    fp.close()
    print ("[ How many tweets : ",len(results),"]")
    #print (results)
    
    
    return results

def GetNewTweetsData(maxnum):
    #how many tweets do you get via Twitter api
    #maxnum = 4000
    
    #Get user info whom you will get tweets from
    user = GetUserFromUserName()
    
    #Clear old text file data.
    ClearTextFile(text_name='all_tweet')
    
    #Get tweets data
    tweets = GetTweet_v02(user,maxnum)
    
    #write down the data, which you will use to find liking user, to a text file
    WriteTweetIdToText(tweets)
    
    return 0


def GetLikingUsers_v02( tweet_ids ):
    results = []
    liking_users = []
    num = 1
    api = GetAuth()
    user_ranking = []
    
    for tweet_id in tweet_ids:
        liking_users = []
        
        time.sleep(2)
        liking_users = ClientInfo().get_liking_users(id=int(tweet_id)).data
        
        
        with open('ranking_user/liking_users.txt','a',encoding='UTF-8') as fp:
            print("\n\n\n",file=fp)
            print ("[",num,"]",file=fp)
            num += 1
            pprint(liking_users,stream=fp)
        fp.close()
        
        if liking_users != None:
            for user in liking_users:
                results.append([user.id, user.name,user.username])
                
            ranking = Ranking_LikingUsers(user_ranking,results)
            results = []
            user_ranking = []
            user_ranking = ranking
    
    return user_ranking


def setName_StrStartEndDate(start,end):
    
    if start[1] < 10 :
        if start[2] < 10 :
            tmp_start_date = str(start[0]) + "0" + str(start[1]) + "0" + str(start[2])
        else :
            tmp_start_date = str(start[0]) + "0" + str(start[1]) + str(start[2])
    else :
        if start[2] < 10 :
            tmp_start_date = str(start[0]) + str(start[1]) + "0" + str(start[2])
        else : tmp_start_date = str(start[0]) + str(start[1]) + str(start[2])
    
    if end[1] < 10 :
        if start[2] < 10 :
            tmp_end_date = str(end[0]) + "0" + str(end[1]) + "0" + str(end[2])
        else :
            tmp_end_date = str(end[0]) + "0" + str(end[1]) + str(end[2])
    else :
        if end[2] < 10 :
            tmp_end_date = str(end[0]) + str(end[1]) + "0" + str(end[2])
        else : tmp_end_date = str(end[0]) + str(end[1]) + str(end[2])
    
    return tmp_start_date,tmp_end_date

def CreateLikingUsersData(start,end):
    tweet_ids = []
    str_print = "aaa"
    
    start_date = datetime.datetime(start[0],start[1],start[2])
    end_date = datetime.datetime(end[0],end[1],end[2])
    
    tmp_start_date,tmp_end_date = setName_StrStartEndDate(start,end)
    
    fileName = "ranking_user/ranking_sorted_"+tmp_start_date+"_"+tmp_end_date+".csv"
    
    print("[ Target period :",start_date,"to",end_date,"]")
    
    ClearTextFile(text_name="liking_users")
    ClearTextFile(text_name="log_test2")
    ClearTextFile(text_name=fileName)
    
    
    tweet_ids = CollectTweetIdsByTime(start_date,end_date)
    
    counted_users = GetLikingUsers_v02(tweet_ids)
    
    with open('ranking_user/ranking.txt','w',encoding='UTF-8') as fp:
        for rank in counted_users:
            pprint(rank,stream=fp)
    fp.close()
    
    ranked_users = sortRank(counted_users)
    
    
    with open(fileName,'a',newline="",encoding='UTF-8') as fp:
        for abc in ranked_users:
            writer = csv.writer(fp)
            writer.writerow(abc)
            #str_print = str(abc[0])+","+str(abc[1])+","+str(abc[2])
            #print(abc,file=fp)
            #print(abc)
            
    fp.close()
    
    return 0

def CollectRankingFileNames():
    results = []
    files = glob.glob("./ranking_user/ranking_sorted_*")
    #pprint (files)
    
    for s in files :
        tmp_a = s.split('\\')
        #pprint (tmp_a)
        results.append(tmp_a[-1])
        
    #pprint (results)
    return results


def ReadRankingSortedFile(f_name):
    
    results = []
    print ("reading file is :",f_name)
    
    tmp_list = []
    
    tmp_str_name = "ranking_user/"+f_name
    
    #pprint(tmp_str)
    
    with open(tmp_str_name,'r',encoding='UTF-8') as fp:
        for tmp_str in fp:
            
            tmp_list = tmp_str.split("\n")
            tmp_list.pop(-1)
            tmp_str = tmp_list[0]
            tmp_list = tmp_str.split(",")
            
            #print (tmp_list)
            #print( len(tmp_list))
            
            
            results.append(tmp_list)
    fp.close()
    
    
    return results


def MergeAllFiles(file_names):
    
    results = []
    #pprint (file_names)
    
    for f_name in file_names :
        #pprint(f_name)
        list_a = ReadRankingSortedFile(f_name)
        results.append(list_a)
    
    #print (len(results))
    
    return results


def CountingMergedFiles(mergedFiles):
    results = []
    flag = 0
    results = mergedFiles.pop(0)
    tmp_i = 0
    
    #pprint (results[0])
    
    for tmp_list in mergedFiles :
        #pprint (tmp_list)
        for user in tmp_list:
            flag = 0
            #print ("user is :",user)
            
            for i in range(len(results)) :
                if user[0] == results[i][0] :
                    #print(user[2], "==", results[i][2])
                    #print(results[i][3], "+", user[3])
                    tmp_i = int(results[i][3]) + int(user[3])
                    results[i][3] = int(tmp_i)
                    #print (tmp_i)
                    flag = 1
                    break
                    #print ("=",results[i][3])
            if flag == 0 :
                results.append(user)
            
    return results


def ExportCvs(results):
    with open('ranking_user/ranking_user.csv','w',newline="",encoding='UTF-8') as fp:
        for user in results :
            writer = csv.writer(fp)
            writer.writerow(user)
    fp.close()
    return 0

def MergeTotalRankingFile() :
    
    results = []
    
    file_names = []
    file_names = CollectRankingFileNames()
    #pprint (file_names)
    
    mergedFiles = []
    
    if len(file_names) != 1 :
        mergedFiles = MergeAllFiles(file_names)
    else :
        print("Total of ranking_sorted file is only one ")
        return 0
    
    merged_users = []
    merged_users = CountingMergedFiles(mergedFiles)
    
    results = sortRank(merged_users)
    
    ExportCvs(results)
    
    return 0

def CheckFolder():
    check_dir = "ranking_user"
    if not os.path.exists(check_dir):
        print("フォルダを作成しました：",check_dir)
        os.makedirs(check_dir)
    return 0
 

def modeSelect():
    mode = 0
    print("\n\n")
    print("1:Get latest Tweets")
    print("2:Start liking ranking")
    print("3:Merge total ranking files")
    
    while True:
        print("\n")
        s = input('Please select mode :')
        #Ignore blank
        s = s.strip()
        print ("You Select :",s)
        if s.isdecimal():
            mode = int(s)
            break
    return mode

   

def main():
    
    maxnum = 4000
    start = [2022,4,10]
    end = [2022,4,19]
    
    #Check argument for mode.
    #If you have argument, skip the mode method
    args = sys.argv
    
    if args[1].isdecimal() != True :
        mode = modeSelect()
    else :
        mode = int(args[1])
    
    CheckFolder()
    if mode == 1:
        GetNewTweetsData(maxnum)
    elif mode == 2:
        CreateLikingUsersData(start,end)
    elif mode == 3:
        MergeTotalRankingFile()
    return 0

main()
