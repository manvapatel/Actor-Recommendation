import json
import pandas as pd
import pickle

file = 'movie.json'
col_names =  ['Title','Actor', 'Genre', 'ActorScore', 'GenreScore', 'FirstYear', 'LastYear', 'UserRating', 'Votes', 'Gross', 'ShortMovie', 'LongMovie', 'NumberofMovies']
# my_df  = pd.DataFrame(columns = col_names)
my_list = []
with open(file) as f:
    json_source = f.read()
    data = json.loads('[{}]'.format(json_source))
    numberofEntries = len(data[0])
    print("Number of Movies is " + str(numberofEntries))
    countg = 0
    counto = 0
    count = 0
    genreCountMax = 5
    actorCountMax = 6

    for i in range(numberofEntries):
        #print(data[0][i]['runtime'])
        #print(data[0][i]['gross'])
        Title = data[0][i]['title']
        Actors = data[0][i]['actors']
        Genres = data[0][i]['genre']
        actorcount = 1
        for actor in Actors:
            genreCount = 1
            for genre in Genres:
                firstYear = data[0][i]['year']
                lastYear = data[0][i]['year']
                userRating = data[0][i]['users_rating']
                votes = data[0][i]['votes']
                gross = data[0][i]['gross']
                runtime = data[0][i]['runtime']
                if not gross:
                    #print("Gross None")
                    countg = countg + 1
                    continue
                if (runtime is None or votes is None or userRating is None or firstYear is None):
                    #print("Other None")
                    counto = counto + 1
                    continue
                count = count + 1
                movieLength = int(runtime[:(len(runtime)-4)])
                my_list.append([Title,actor, genre , actorcount, genreCount, int(firstYear), int(lastYear), float(userRating), int(votes.replace(',','')), int(gross[1:].replace(',','')), 0 if movieLength>100 else 1, 1 if movieLength>100 else 0,1])

                # my_df.append([actor, genre , actorcount, genreCount, int(firstYear), int(lastYear), float(userRating), int(votes.replace(',','')), int(gross[1:].replace(',','')), 0 if movieLength>100 else 1, 1 if movieLength>100 else 0,1])
                # print(my_df.head())
                # if (len(my_df) % 100 == 0):
                    # print(len(my_df))
                genreCount = genreCount + 1
                if(genreCount == genreCountMax):
                    break
            actorcount = actorcount + 1
            if(actorcount == actorCountMax):
                break
    print(countg)
    print(counto)
    print(count)
my_df  = pd.DataFrame(my_list, columns = col_names)
print(my_df.columns)

my_df = my_df.sort_values(["Actor","Genre"])
#print(my_df2.head())

temp1 = my_df[['Actor','NumberofMovies','ShortMovie','LongMovie']].groupby('Actor').agg({'NumberofMovies': 'sum','ShortMovie': 'sum','LongMovie': 'sum'})

print(temp1.head())

temp2 = my_df.drop(['NumberofMovies','ShortMovie','LongMovie'],axis=1)

GenreActor_IndividualMovie = pd.merge(temp2,temp1, on = 'Actor', how='left')

print(GenreActor_IndividualMovie.head())

pickle.dump( GenreActor_IndividualMovie, open( "save_genActor.p", "wb" ) )


#print(my_df2.loc[my_df2['Actor'] == "Christian Bale"])
#print(len(my_df["Actor"].unique()))
print('------------------------------')
GenreActor_Group = my_df.groupby(['Actor', 'Genre']).agg({'ActorScore':'mean',
                                                 'GenreScore':'mean',
                                                 'FirstYear': 'min',
                                                 'LastYear':'max',
                                                 'UserRating':'mean',
                                                 'Votes': 'mean',
                                                 'Gross': 'mean',
                                                 'ShortMovie': 'sum',
                                                 'LongMovie': 'sum',
                                                 'NumberofMovies': 'sum'})
print(GenreActor_Group.head())

