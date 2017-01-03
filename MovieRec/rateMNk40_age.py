import random
import math
import operator

# START FILE HANDLING CODE#
# start read from user file user lists
f = open('u.user', 'r')
uuser = list()
uuser = f.readlines()
f.close()
# start read from user file user lists

# start read from u1.base file
f = open('u1.base', 'r')
u1base = list()
u1base = f.readlines()
f.close()
# start read from u1.base file

# start read from u1.test file
f = open("u1.test", "r")
u1test = list()
u1test = f.readlines()
f.close()
# end read from u1.test file

# start read from data file movie lists
f = open('u.item', 'r')
uitem = list()
uitem = f.readlines()
f.close()
# end read from data file movie lists

# start read from data file user movie mapping
f = open('u.data', 'r')
udata = list()
udata = f.readlines()
f.close()
# end read from data file user movie mapping
# END FILE HANDLING CODE#

# START POPULATING DATASTRUCTURES
# start get all users list from u.user
users = list()
usertable = dict()
for c_user in range(0, len(uuser)):                             # split by | for uuser
    splitlist = uuser[c_user].split('|')
    users.append(splitlist[0])
    usertable[splitlist[0]] = list(splitlist)
# end get all users list from u.user

#print usertable
# start get all movies list from u.item
movies = list()
for c_movie in range(0, len(uitem)):
    movies.append(uitem[c_movie].split('|')[0])                 # split by | for uitem
# end get all movies list from u.item

# start mapping userid, movieid for watched movies
usermoviewatched = dict()                                       # dictionary with userid as key
for i in range(0, len(u1base)):
    userid = u1base[i].split('\t')[0]
    movieid = u1base[i].split('\t')[1]                           # split by \t for u1base
    if userid not in usermoviewatched:
        uselist = list()
        uselist.append(movieid)
        usermoviewatched[userid] = uselist
    else:
        tempList = list()
        tempList = usermoviewatched[userid]
        tempList.append(movieid)
        usermoviewatched[userid] = tempList

#for usermovie in usermoviewatched:
#    print usermovie, "\t", usermoviewatched[usermovie]
#print usermoviewatched
movieuserwatched = dict()                                       # dictionary with movieid as key
for i in range(0, len(udata)):
    userid = udata[i].split('\t')[0]
    movieid = udata[i].split('\t')[1]                           # split by \t for udata
    if movieid not in movieuserwatched:
        uselist = list()
        uselist.append(userid)
        movieuserwatched[movieid] = uselist
    else:
        tempList = list()
        tempList = movieuserwatched[movieid]
        tempList.append(userid)
        movieuserwatched[movieid] = tempList
# end mapping userid, movieid for not watched movies

# start mapping userid, movieid for not watched movies
#usermovieNotwatched = dict()                                       # dictionary with movied as key
#for userid in users:
    #for movieid in movies:
        #if movieid not in usermoviewatched[userid]:
            #if userid not in usermovieNotwatched:
               # uselist = list()
              #  uselist.append(movieid)
              #  usermovieNotwatched[userid] = uselist
            #else:
              #  tempList = list()
              #  tempList = usermovieNotwatched[userid]
              #  tempList.append(movieid)
              #  usermovieNotwatched[userid] = tempList

usermovieNotwatched = dict()                                       # dictionary with movied as key
for u1testitem in u1test:
    u1testitemsplit = u1testitem.split('\t')
    userid = u1testitemsplit[0]
    movieid = u1testitemsplit[1]
    if movieid not in usermoviewatched[userid]:
        if userid not in usermovieNotwatched:
            uselist = list()
            uselist.append(movieid)
            usermovieNotwatched[userid] = uselist
        else:
            tempList = list()
            tempList = usermovieNotwatched[userid]
            tempList.append(movieid)
            usermovieNotwatched[userid] = tempList

movieuserNotwatched = dict()                                       # dictionary with movied as key
for movieid in movies:
    for userid in users:
        if userid not in movieuserwatched[movieid]:
            if movieid not in movieuserNotwatched:
                uselist = list()
                uselist.append(userid)
                movieuserNotwatched[movieid] = uselist
            else:
                tempList = list()
                tempList = movieuserNotwatched[movieid]
                tempList.append(userid)
                movieuserNotwatched[movieid] = tempList

# end mapping userid, movieid for not watched movies

# start usermovierating mapping
usermovierateddata = dict()
for i in range(0, len(udata)):
    splitarray = udata[i].split('\t')
    userid = splitarray[0]
    movieid = splitarray[1]
    rating = splitarray[2]

    usermovieStrPairKey = str(userid) + "#" + str(movieid)
    usermovierateddata[usermovieStrPairKey] = rating
# end usermovierating mapping

# END POPULATING DATASTRUCTURES

# BEGIN FUNCTION DEFINITIONS

def findEuclideanDist(listcurruserrating, listcommuserrating):
    retsum = 0
    for i in range(0, len(listcurruserrating)):
        retsum += (int(listcurruserrating[i]) - int(listcommuserrating[i])) * (int(listcurruserrating[i]) - int(listcommuserrating[i]))
    return math.sqrt(retsum)

def findManhattanDist(listcurruserrating, listcommuserrating):
    retsum = 0
    for i in range(0, len(listcurruserrating)):
        retsum += int(listcurruserrating[i]) - int(listcommuserrating[i])
    return retsum

def findLmaxDist(listcurruserrating, listcommuserrating):
    retmaxdist = 0
    for i in range(0, len(listcurruserrating)):
        idist = (int(listcurruserrating[i]) - int(listcommuserrating[i])) * (int(listcurruserrating[i]) - int(listcommuserrating[i]))
        retmaxdist = max(idist, retmaxdist)
    return retmaxdist

def getleastKdistances(userID, currvscommuserratingdifflist, k):
    currvscommuserratingdifflist_sorted = sorted(currvscommuserratingdifflist.items(), key=operator.itemgetter(1))

    if k > len(currvscommuserratingdifflist_sorted):
        k = len(currvscommuserratingdifflist_sorted)  # to avoid index out of bound errors

    listMinValueKeys = list()
    for i in range(0, k):
        try:
            splitdata = currvscommuserratingdifflist_sorted[i][0].split("@")
            useridsplit = splitdata[0]
            usertousesplit = splitdata[1]
            if useridsplit == userID and usertousesplit not in listMinValueKeys:
                listMinValueKeys.append(usertousesplit)
        except IndexError:
            pass
    return listMinValueKeys

currvscommuserratingdiffdictEU = dict()
currvscommuserratingdiffdictMN = dict()
currvscommuserratingdiffdictLM = dict()
mostsimilarUsers = dict()
# this function calculates the distances between the movie ratings of the given user with respect all other users
# for every user in users
# for all movies the user didn't watch
# find k users who did watch
def getSimilarUsers(userid, userslist, k):
    # get a random 20 users based on random number generator
    # newlist = list([random.uniform(0, len(userslist)) for i in range(len(userslist))])
    # find their distances of rating attribute with those of userid
    # get 10 similar users
    iusercount = 0
    retUsersList = list()

    k = min(k, len(userslist))
    for icounter in range(0, k):
        iUser = userslist[icounter]
        if iUser not in retUsersList and iUser != userid:
            try:
                commonMovies = list(set(usermoviewatched[userid]).intersection(usermoviewatched[iUser]))
                if len(commonMovies) > 0:
                    listcurrusercommmoviesrating = list()
                    listcommusercommoviesrating = list()
                    for commonMovie in commonMovies:
                        currusermoviekey = str(userid) + "#" + str(commonMovie)
                        currentuserrating = usermovierateddata[currusermoviekey]
                        listcurrusercommmoviesrating.append(currentuserrating)
                        listcurrusercommmoviesrating.append(usertable[userid][1])   #adding user age as another factor

                        commusermoviekey = str(iUser) + "#" + str(commonMovie)
                        commonuserrating = usermovierateddata[commusermoviekey]
                        listcommusercommoviesrating.append(commonuserrating)
                        listcommusercommoviesrating.append(usertable[userid][1])    #adding user age as another factor

                    currcommuserstrkey = userid + "@" + iUser

                    # Below three are the training data based on euclidean, manhattan and lmax distances
                    currvscommuserratingdiffdictEU[currcommuserstrkey] = findEuclideanDist(listcurrusercommmoviesrating, listcommusercommoviesrating)
                    currvscommuserratingdiffdictMN[currcommuserstrkey] = findManhattanDist(listcurrusercommmoviesrating, listcommusercommoviesrating)
                    currvscommuserratingdiffdictLM[currcommuserstrkey] = findLmaxDist(listcurrusercommmoviesrating, listcommusercommoviesrating)
                iusercount += 1
            except KeyError:
                pass
    mostsimilarUsers[userid] = getleastKdistances(userid, currvscommuserratingdiffdictMN, k)
    retUsersList = mostsimilarUsers
    return retUsersList

r = dict()
def getRating(userid, movietoberated, similarusers):
    ratingtobegiven = 0
    n_similarUsers = len(similarusers) - 1
    if n_similarUsers > 1:
        for similaruser in similarusers:
            if similaruser != userid:
                usermovieStrPairKey = str(similaruser) + "#" + str(movietoberated)
                try:
                    ratingtobegiven += int(usermovierateddata[usermovieStrPairKey])
                    r[usermovieStrPairKey] = 1
                except KeyError:
                    ratingtobegiven += random.choice([1, 2, 3, 4, 5])
                    r[usermovieStrPairKey] = 0
                    pass
        ratingtobegiven = ratingtobegiven/n_similarUsers
    else:
        ratingtobegiven = 3
    return ratingtobegiven
# END FUNCTION DEFINITIONS

# BEGIN MAIN PROGRAM
usermovieNotwatchedUsersWatched = dict()
predicteduserrating = dict()
f = open("u1.predictedtest", 'w')
for userid in usermovieNotwatched:
    movieidsNotwatched = usermovieNotwatched[userid]
    usersWhowatched = list()
    similarusers = list()
    k = 40                  # need at least 20 similar people
    for everyMovieNotWatched in movieidsNotwatched:
        usersWhowatched = movieuserwatched[everyMovieNotWatched]
        similarusers = getSimilarUsers(userid, usersWhowatched, k)
        usermoviestrkey = str(userid) + "#" + str(everyMovieNotWatched)

        if len(similarusers) > 0:
            predicteduserrating[usermoviestrkey] = getRating(userid, everyMovieNotWatched, similarusers[userid])
        else:
            predicteduserrating[usermoviestrkey] = getRating(userid, everyMovieNotWatched, usersWhowatched)

# Predict new ratings and push them into file
for eachUserMovieRating in predicteduserrating:
    splitarr = eachUserMovieRating.split('#')
    user = splitarr[0]
    movie = splitarr[1]
    f.write(str(user) + "\t" + str(movie) + "\t" + str(predicteduserrating[eachUserMovieRating]) + "\n")
f.close()
# note: predicted test file will have 1506126 rows adding 80000 rows from u1.base must give total number of user-movie combinations

u1testlist = list()
for i in range(0, len(u1test)):
    splitarr = u1test[i].split('\t')
    userid = splitarr[0]
    movieid = splitarr[1]
    rating = splitarr[2]
    timestamp = splitarr[3]
    u1testlist.append(splitarr)

for i in range(0, len(u1testlist)):
    uid = u1testlist[i][0]
    mid = u1testlist[i][1]
    rt  = u1testlist[i][2]

    struidmidkey = str(uid) + "#" + str(mid)
    u1testlist[i].append(predicteduserrating[struidmidkey])

numerator = 0
denominator = 0
for i in range(0, len(u1testlist)):
    u = u1testlist[i][0]
    m = u1testlist[i][1]
    strum = str(u) + "#" + str(m)
    tij = int(u1testlist[i][2])
    pij = int(u1testlist[i][4])
    rij = 0
    try:
        rij = int(r[strum])
    except KeyError:
        rij = 0

    numerator += float(rij * abs(float((pij - tij))))
    denominator += float(rij)

MADNaive = numerator/denominator
print MADNaive

#END MAIN PROGRAM