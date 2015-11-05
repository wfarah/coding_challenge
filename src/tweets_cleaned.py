# example of program that calculates the number of tweets cleaned

n_unicode=0 #Number of tweets containing unicodes
data=[] #tweets + timestamps

with open("tweet_input/tweets.txt","r") as input_file:
	for line in input_file:
		l=line.split(',"') #split line at every ',"'
		n_time,n_tweet=-1,-1
		for i in range(0,len(l)):
			if "created_at" in l[i]:
				n_time=i 	#n_time is where the time is in the splitted line
			elif "text" in l[i]:
				n_tweet=i	#n_tweet is where the tweet is in the splitted line
			if n_time!=-1 and n_tweet!=-1:
				break
		if n_time==-1 and n_tweet==-1:	#This is not a tweet, skipping it		
			continue
		timestamp=l[n_time].split('"created_at":"')[1][:-1] #The cleaned time of tweet
		tweet=l[n_tweet].split('text":"')[1][:-1]
		tweet_cleaned=tweet.decode('unicode_escape').encode('ascii','ignore')
		if tweet_cleaned!=tweet:	#Test for unicode
			n_unicode+=1
		cleaning_dic={"\/":"/" , "\\\\":"\\" , "\'":"'" , '\"':'"' , "\n":" " , "\t":" "}	#dictionary for cleaning tweets
		for i,j in cleaning_dic.iteritems():
			tweet_cleaned=tweet_cleaned.replace(i,j)
		data.append(tweet_cleaned+" (timestamp: "+timestamp+")")

with open("tweet_output/ft1.txt","w") as output_file:
	for i in data:
		output_file.write(i+"\n")
	output_file.write("\n"+str(n_unicode)+" tweets contained unicode")
