from music2class import * #importing my now OOC's music2 class (not neccesary for GA function, but can be used to play the final result/selected samples)
import random #import random selection
import math #import math for abs()
music = music2() #instantiate music2 as music (not neccesary for GA function, but can be used to play the final result/selected samples)
intervals = [] #Stores the interval values 1-101 that my music2 class can handle
for i in range(0,102): #grab integer values 1-101...
	intervals.append(i) #...and append them to the list we have to select from
lengths = [8] #note length limited to eighth notes for now
masterArray = [] #Master array to store all of the random data set
#Master Array Key: [averaged total score, [intervals], [lengths], pitch variety score, pitch range score,Dissonance score]
for x in range(0,1001):#create 1000 randomly seeded phrases

	#relevant value initialization
	interiorArray = [] #contains values to be stored in master array
	noteArray = [] #stores notes generated randomly
	lengthArray = [] #stores lengths generated randomly
	pitchVarietyScore = 0 #stores the calculated pitch variety score (Towsey et al.)
	pitchRangeScore = 0 #stores the pitch range score (Towsey et al.)
	dissonanceScore = 0 #stores the dissonance score (Towsey et al.)
	averagedScore = 0 #average of all three scores
	#random note selection
	for j in range(0,20): #create groupings of 20 notes for a phrase
		randInterval = random.choice(intervals)#choose randomly from the intervals list
		randLength = random.choice(lengths) #choose randomly from the lengths list (currenly set to 8ths only)
		noteArray.append(randInterval) #append the resulting note to the phrase's noteArray
		lengthArray.append(randLength) #append the resulting note to the phrase's lengthArray
			
			
	#dissonance score calculation THIS MUST BE FIXED DUE TO ISSUE: TBD: Whether I'm looking at a random distriribution or this algorithm is broken see line 44
	baseInterval = noteArray[0] #stores the very first note of the phrase for dissonance analysis, mostly because we can't analyze the dissonance between the first note of the phrase and the note before it
	dissonanceSum = 0 #value obtained by summing all the dissonance ratings of adjacent pitches
	for i in range(1, len(noteArray)): #starting from the second value to the end of the note array:
		for j in range(-4,5): #to catch different octaves, multiply the output of this function bu twelve. This results in a range along the full keyboard
			if(noteArray[i-1] - noteArray[i] == -2+12*j): #use noteArray[i-1] - noteArray[i]. An interval of 10 is considered moderately dissonant (Towsey et al.) a +10 is tonally equivalent to a -2 shift
				dissonanceRating = 0.5#moderate dissonance is awarded a score of 0.5
				#print("Caught moderate dissonance of : "+str(noteArray[i-1])+" and "+str(noteArray[i])) #test case for moderate dissonance
				break#if dissonance is detected, no reason to check the rest of the keyboard
			elif(noteArray[i-1] - noteArray[i] == abs(6)+12*j or (noteArray[i-1] - noteArray[i]) == abs(11)+12*j or (noteArray[i-1] - noteArray[i]) ==abs(13)+12*j):#use noteArray[i-1] - noteArray[i]. An interval of 6 11 or 13 is considered highly dissonant (Towsey et al.). This should be noted: A +12 and -13 will be equivalent, and vice versa. Because there are 12 half steps in a full octave, +-6 and -+6 will also similarly cancel out
				#print("Caught extreme dissonance of : "+str(noteArray[i-1])+" and "+str(noteArray[i]))
				dissonanceRating = 1.0#highly dissonant intervals are awarded a score of 1.0
				break#if dissonance is detected, no reason to check the rest of the keyboard
			else:#all other intervals are fairly assonant...
				dissonanceRating = 0#...and are therefore awarded a score of zero. This does not cound minors etc as notably dissonant.
				#no break here, as no dissonance is detected in this octave, but there might be in others    <--This may have fixed it
		dissonanceSum=dissonanceSum+dissonanceRating#Add the running dissonance sum to
	dissonanceScore = (dissonanceSum/20) #final score is equal to the average of all dissonant intervals
	
	#note range score calculation
	maxValue = -1 #set the minValue to one below the absolute minimum note value
	for i in noteArray: #for each note
		if i > maxValue: #if it's greater than the current max value
			maxValue = i #set it as the max value
	minValue = maxValue #set the minimum value to the absolute maximum value in the set
	for i in noteArray: #for each note
		if i < minValue: # if it's less than the current minimum value
			minValue = i #set it as the minimum
	pitchRange = (maxValue-minValue)#sets the range from bottom to top pitch
	if(pitchRange <=5): #if there's almost no pitch variety in range:
		pitchRangeScore = 0 # score a zero
	if(pitchRange <= 11):#if there's some variety:
		pitchRangeScore = 0.5 #score a half
	if(pitchRange >=25): #if there's a bit too much variety:
		pitchRange = 0.5 #score a half
	if(pitchRange >= 37): #if the computer's all over the goddamn keyboard:
		pitchRangeScore = 0 #score a zero
	if(pitchRange <= 25 and pitchRange >= 11): #if the computer hit right around 2 octaves used:
		pitchRangeScore = 1 #score a one
	
	#pitch variety score calculation
	usedPitchArray = []#declare an empty array to store pitches we've already used
	for i in noteArray:	 #for each interval
		if i not in usedPitchArray: #if it's not in the used pitch array
			usedPitchArray.append(i) #add it
	pitchesUsed = len(usedPitchArray) #pitches used will be then the length of the usedPitchArray
	pitchVarietyScore = (pitchesUsed/20.0)#the final score is the unique pitches per pitch played
	
	#average all three scores:
	averagedScore = ((pitchVarietyScore+pitchRangeScore)/2)-dissonanceScore
	#appending data to the interiorArray
	interiorArray.append(averagedScore)
	interiorArray.append(noteArray)
	interiorArray.append(lengthArray)
	interiorArray.append(pitchVarietyScore)
	interiorArray.append(pitchRangeScore)
	interiorArray.append(dissonanceScore)
	#and finally, append the interior array to the master array:
	masterArray.append(interiorArray)

#now that we have our first random data set, sort it and print it to debug
#for i in sorted(masterArray): #and just to make sure everything's peachy
	#print(i) #print every value from the master array
masterArray = sorted(masterArray) #sort the masterArray by the first value in each phraseArray, the averaged score. Maximum score is a 1. Array will sort worst[0] best[len()-1]

#################################
#       NATURAL SELECTION       #
#################################

#prepare to kill off the weaklings
markedForRemove = [] #declare a list to store the indexes of the phrases which are deemed inadequate
for i in range(0,len(masterArray)): #for each value in the sorted masterArray
	randVal = random.randint(1,100) #get a random seed value 1-100 inclusive
	if(i > 500): #if we're in the top 50% of phrases
		if randVal >= 97: #give them a 3% chance to be deleted
			markedForRemove.append(i) #append the unlucky ones' indexes to markedForRemove
	else: #otherwise, we're in the bottom 50%
		if randVal <= 97: #and they have a 97% chance to be deleted
			markedForRemove.append(i) #append the unlucky ones to the removal list
i = len(markedForRemove)-1 #get ready to iterate backwards over markedForRemove

#kill off the weaklings
while i >= 0: #until we run through index zero
	#print("Deleting index " + str(markedForRemove[i]) + " with score of "+ str(masterArray[markedForRemove[i]][0])) #debug message, show the overall rank and overall score
	del masterArray[markedForRemove[i]] #delete the marked index from master, iterating backwards so we don't get an 'accordion', where indexes fall into the voids created by other indexes and just generally cause problems
	i = i - 1#decrement the iterator

for asdfg in range(0,100001):
	#relevant value initialization
	for qwert in range(0,1001-len(masterArray)): #pad masterArray with the parent entities keeping in mind that not always 500 phrases will be killed. basically the parents divide before evolving further
		masterArray.append(masterArray[qwert]) #pad it good
	#random note evolution
	for i in range(0, len(masterArray)): #for each of the values in masterArray
		for j in range(0, len(masterArray[i][1])): #for each of the notes in masterArray[i]
			randVal = random.randint(1,100) #grab a random number 1,100 inclusive
			if randVal >= 60: #there is a 40% chance to...
				masterArray[i][1][j] = random.choice(intervals)#evolve new notes            EVOLUTION ISSUE: Will evolve to generate good variety of tonally accurate notes all over the keyboard. Need a solution to evolving notes that further incentivizes limited range
			if randVal >= 90: #there is a 10% chance to...
				masterArray[i][2][j] = random.choice(lengths)#evolve new lengths
		noteArray = masterArray[i][1]#set noteArray equal to this phrase's note array
		lengthArray = masterArray[i][2]#set lengthArray equal to this phrase's lenght array
		pitchVarietyScore = 0 #stores the calculated pitch variety score (Towsey et al.)
		pitchRangeScore = 0 #stores the pitch range score (Towsey et al.)
		dissonanceScore = 0 #stores the dissonance score (Towsey et al.)
		averagedScore = 0 #average of all three scores
		
		#dissonance score calculation 
		baseInterval = noteArray[0] #stores the very first note of the phrase for dissonance analysis, mostly because we can't analyze the dissonance between the first note of the phrase and the note before it
		dissonanceSum = 0 #value obtained by summing all the dissonance ratings of adjacent pitches
		for i in range(1, len(noteArray)): #starting from the second value to the end of the note array:
			for j in range(-4,5): #to catch different octaves, multiply the output of this function bu twelve. This results in a range along the full keyboard
				if(noteArray[i-1] - noteArray[i] == -2+12*j): #use noteArray[i-1] - noteArray[i]. An interval of 10 is considered moderately dissonant (Towsey et al.) a +10 is tonally equivalent to a -2 shift
					dissonanceRating = 0.5#moderate dissonance is awarded a score of 0.5
					#print("Caught moderate dissonance of : "+str(noteArray[i-1])+" and "+str(noteArray[i])) #test case for moderate dissonance
					break#if dissonance is detected, no reason to check the rest of the keyboard
				elif(noteArray[i-1] - noteArray[i] == abs(6)+12*j or (noteArray[i-1] - noteArray[i]) == abs(11)+12*j or (noteArray[i-1] - noteArray[i]) ==abs(13)+12*j):#use noteArray[i-1] - noteArray[i]. An interval of 6 11 or 13 is considered highly dissonant (Towsey et al.). This should be noted: A +12 and -13 will be equivalent, and vice versa. Because there are 12 half steps in a full octave, +-6 and -+6 will also similarly cancel out
					#print("Caught extreme dissonance of : "+str(noteArray[i-1])+" and "+str(noteArray[i]))
					dissonanceRating = 1.0#highly dissonant intervals are awarded a score of 1.0
					break#if dissonance is detected, no reason to check the rest of the keyboard
				else:#all other intervals are fairly assonant...
					dissonanceRating = 0#...and are therefore awarded a score of zero. This does not cound minors etc as notably dissonant.
					#no break here, as no dissonance is detected in this octave, but there might be in others
			dissonanceSum=dissonanceSum+dissonanceRating#Add the running dissonance sum to
		dissonanceScore = (dissonanceSum/20) #final score is equal to the average of all dissonant intervals
		
		#note range score calculation
		maxValue = -1 #set the minValue to one below the absolute minimum note value
		for i in noteArray: #for each note
			if i > maxValue: #if it's greater than the current max value
				maxValue = i #set it as the max value
		minValue = maxValue #set the minimum value to the absolute maximum value in the set
		for i in noteArray: #for each note
			if i < minValue: # if it's less than the current minimum value
				minValue = i #set it as the minimum
		pitchRange = (maxValue-minValue)#sets the range from bottom to top pitch
		if(pitchRange <=5): #if there's almost no pitch variety in range:
			pitchRangeScore = 0 # score a zero
		if(pitchRange <= 11):#if there's some variety:
			pitchRangeScore = 0.5 #score a half
		if(pitchRange >=25): #if there's a bit too much variety:
			pitchRange = 0.5 #score a half
		if(pitchRange >= 37): #if the computer's all over the goddamn keyboard:
			pitchRangeScore = 0 #score a zero
		if(pitchRange <= 25 and pitchRange >= 11): #if the computer hit right around 2 octaves used:
			pitchRangeScore = 1 #score a one
		
		#pitch variety score calculation
		usedPitchArray = []#declare an empty array to store pitches we've already used
		for i in noteArray:	 #for each interval
			if i not in usedPitchArray: #if it's not in the used pitch array
				usedPitchArray.append(i) #add it
		pitchesUsed = len(usedPitchArray) #pitches used will be then the length of the usedPitchArray
		pitchVarietyScore = (pitchesUsed/20.0)#the final score is the unique pitches per pitch played
		
		#average all three scores:
		averagedScore = ((pitchVarietyScore+pitchRangeScore)/2)-dissonanceScore
		#rather than appending, this time update the values of each masterArray location
		masterArray[i][0] = averagedScore
		masterArray[i][1] = noteArray
		masterArray[i][2] = lengthArray
		masterArray[i][3] = pitchVarietyScore
		masterArray[i][4] = dissonanceScore
		
	
	#Sort our brand new population
	masterArray = sorted(masterArray) #sort the masterArray by the first value in each phraseArray, the averaged score. Maximum score is a 1. Array will sort worst[0] best[len()-1]
	#for i in masterArray: #and for each entry in the now sorted array
		#print i #print it
	#################################
	#       NATURAL SELECTION       #
	#################################
	
	#prepare to kill off the weaklings
	markedForRemove = [] #declare a list to store the indexes of the phrases which are deemed inadequate
	for i in range(0,len(masterArray)): #for each value in the sorted masterArray
		randVal = random.randint(1,100) #get a random seed value 1-100 inclusive
		if(i > 500): #if we're in the top 50% of phrases
			if randVal >= 97: #give them a 3% chance to be deleted
				markedForRemove.append(i) #append the unlucky ones' indexes to markedForRemove
		else: #otherwise, we're in the bottom 50%
			if randVal <= 97: #and they have a 97% chance to be deleted
				markedForRemove.append(i) #append the unlucky ones to the removal list
	i = len(markedForRemove)-1 #get ready to iterate backwards over markedForRemove
	
	#kill off the weaklings
	while i >= 0: #until we run through index zero
		#print("Deleting index " + str(markedForRemove[i]) + " with score of "+ str(masterArray[markedForRemove[i]][0])) #debug message, show the overall rank and overall score
		del masterArray[markedForRemove[i]] #delete the marked index from master, iterating backwards so we don't get an 'accordion', where indexes fall into the voids created by other indexes and just generally cause problems
		i = i - 1#decrement the iterator
	print("Completed Generation :: "+ str(asdfg))
	print("\n---------------------------\nThe winning value for this generation was :: ")
	print(str(masterArray[len(masterArray)-1])+"\n\n")
	if(masterArray[len(masterArray)-1][0] > 0.5):
		print("Broke the .5 barrier")
		raise Exception
	