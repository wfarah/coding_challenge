# example of program that calculates the average degree of hashtags

import time
import re
import itertools

def get_info(l):
	"""Function that returns tweets and timestamp from lines from tweet.txt"""
	l=l.split(',"') #split line at every ',"'
	n_time,n_tweet=-1,-1
	for i in range(len(l)):
		if "created_at" in l[i]:
			n_time=i 	#n_time is the index where the time is in the splitted line
		elif "text" in l[i]:
			n_tweet=i	#n_tweet is the index where the tweet is in the splitted line
		if n_time!=-1 and n_tweet!=-1:
			break
	if n_time==-1 and n_tweet==-1:			
		return None,None	#Not a tweet
	timestamp=l[n_time].split('"created_at":"')[1][:-1] #The cleaned time of tweet
	tweet=l[n_tweet].split('text":"')[1][:-1]	#extracting tweet
	tweet=tweet.decode('unicode_escape').encode('ascii','ignore') #removing unicode characters
	cleaning_dic={"\/":"/" , "\\\\":"\\" , "\'":"'" , '\"':'"' , "\n":" " , "\t":" "}	#dictionary for escape characters tweets
	for i,j in cleaning_dic.iteritems():	#replacing escape characters
		tweet=tweet.replace(i,j)
	return tweet,timestamp

def extract_hashtags(tweet):
	"""Function to extract tweets, supposedly hashtags are separated by an empty space. eg: tweet='#python is a cool #programming #language', returns ['python','programming','language']. Another function corrects in case the hashtags do not end with an empty space (see test_hashtag() function)"""
	tweet_split=tweet.split("#")
	if len(tweet_split) is 1:	#When =1 means no hastags
		return None
	else:	#When different than 1, means at least 1 hashtag exists
		hashtags=[]
		for i in range(1,len(tweet_split)):	
			if tweet_split[i].split(" ")[0] is "": continue #Filter out an empty hashtag, in rare case where tweet ends with a "#"
			t=tweet_split[i].split(" ")[0]
			hashtags.append(t.lower()) #lower makes all strings lower case, hashtags are not case-sensitive
		if hashtags==[]: return None	#Removing empty hashtags, resulted from only unicode characters
		hashtags=list(set(hashtags))	#to select distinct hashtags
		hashtags.sort()	#Sorted in alphabatical order to avoid 2 nodes like ["a","b"] and ["b","a"] being different
		return test_hashtags(hashtags)

def test_hashtags(hashtags):
	"""Function to test if extracted hashtags are correct, i.e special character-free. eg: if tweet is tweet='#python(my favorite #language)', extract_hashtags(tweet) will output ['python(my','language)']. This function corrects for this, takes the hashtags as input and returns ['python','language']. It works for all special characters except underscores"""
	n=len(hashtags)	#number of hashtags
	correct_hashtags=[]
	for i in range(n):
		match=re.search('[^a-zA-Z0-9\\\\_]',hashtags[i])	#Checks if any special character exists, except for '_' and '\\\\' for unicode characters
		if match:
			correct_hashtags.append(hashtags[i][:match.start()])	#cut hashtag before special character.
		else:
			correct_hashtags.append(hashtags[i])	#no special character, hashtag is the same
	return correct_hashtags
	

def convert_to_epoch(timestamp):
	"""Function to convert the current timestamp to epoch time to make timestamp of tweets comparable"""
	t=timestamp.split(" ")
	timestamp_newformat=t[2]+"."+t[1]+"."+t[5]+" "+t[3]	#New format for time: day.month.year hour:min:sec
	time_epoch=time.mktime(time.strptime(timestamp_newformat, "%d.%b.%Y %H:%M:%S"))	#convert to epoch
	return time_epoch


def calculate_avg_deg(all_edge_lists):
	"""Function that returns the average degree of all nodes"""
	hashtags_list=[]
	for i in all_edge_lists:	#converting the edge_list from a list of tuples to a list of strings
		hashtags_list.append(i[0])
		hashtags_list.append(i[1])
	nodes=list(set(hashtags_list))	#nodes are the unique hashtags in the edge list
	n_nodes=len(nodes)
	#print n_nodes
	deg_all_nodes=2*len(all_edge_lists)	#the degree of all nodes combined is twice the number of edges!
	avg_deg=float(deg_all_nodes)/n_nodes	#calculating the average degree of all nodes
	return avg_deg





#######################################################		MAIN			#######################################################




input_file=open("tweet_input/tweets.txt","r")	#tweets input file

edgelist_dict={}	#dictionary to store the edgelists. timestamp in epoch times are the keys, whereas a list of edges are the values. example: edgelist_dict={1446212051.0:[('hello','hi')] , 1446212052.0:[('python','programming'),('python','language'),('python','language')]}

time_window=60	#time window to reject tweets

for line in input_file:
	tweet,timestamp=get_info(line)
	if tweet is None and timestamp is None:	#Rejecting none tweets
		continue
	hashtags=extract_hashtags(tweet)	#attempting to extract hashtags from tweet
	if hashtags is None or hashtags is [] or len(hashtags) is 1:	#rejecting only 1 or no hashtags at all
		continue
	else:		#2 or more hashtags exist in tweet, proceed to processing
		timestamp_epoch=convert_to_epoch(timestamp)	#converting time to seconds
		current_edge_list=[x for x in list(itertools.combinations(hashtags,2))]	#creating edge list for new tweet, example: hashtags=["a","b","c"] then current_edge_list=[("a,b"),("a","c"),("b","c")]
		if timestamp_epoch in edgelist_dict:
			edgelist_dict[timestamp_epoch].extend(current_edge_list)	#if timestamp exists in dictionary. i.e tweets posted at the same time, knowing that the smallest time tick available is 1 second
		else:
			edgelist_dict.update({timestamp_epoch:current_edge_list})	#tweet posted at a new timestamp is added to dictionary
		to_delete=[x for x in edgelist_dict.keys() if timestamp_epoch-x > time_window]	#timestamps(keys) that fall outside the 60 seconds timewindow
		for i in to_delete:	#deleting the values of edgelist_dict that fall outside the 60s window
			del edgelist_dict[i]
		all_edge_lists=[]
		for i in edgelist_dict.itervalues():
			all_edge_lists.extend(i)	#This is all the edge-lists for time window of 60 seconds
		all_edge_lists=list(set(all_edge_lists))	#filtering out possible same edgelist
		avg_deg=calculate_avg_deg(all_edge_lists)	#calculating average degree
		with open("tweet_output/ft2.txt","a") as output:
			output.write(str(round(avg_deg,2))+"\n")	#appending the rolling average degree to ft2.txt file


		"""WARNING: IF EXECUTED MORE THAN ONCE, WILL KEEP APPENDING TO OUTPUT FILE"""
input_file.close()

