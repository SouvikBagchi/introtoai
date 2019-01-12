import math
import re

#Define a set function since we cannot use the inbuilt set function :/
class Set:

  def __init__(self):

    self.elements = []

  def add(self,x):
    if x not in self.elements : self.elements.append(x)

  def len(self):
    return len(self.elements)

  def all_elements(self):

    element_list = []
    for e in self.elements:
      element_list.append(e)

    return element_list



class Bayes_Classifier:

    def __init__(self):

        #total_count holds the total outcomes till now
        self.total_count = 0

        self.review_type_1 = None
        self.review_type_2 = None

        self.total_type_1_review = 0
        self.total_type_2_review = 0

        #create a list of word list associated with the types and count their frequency
        self.type_1_word_list = {}
        self.type_2_word_list = {}

        self.prob_type_1 = 0.0
        self.prob_type_2 = 0.0

        self.add_one_smooth_type_1 = 0.0
        self.add_one_smooth_type_2 = 0.0


    #this function only processes text and returns it
    def text_process(self, text):


        #list of stop words
        stop_words = ["a","about","above","after","again","all","am","an","and","any","are","as","at","be","because",
        "been","before","being","below","between","both","but","by","could","did","do","does","doing","down","during","each",
        "few","for","from","further","had","has","have","having","he","he’d","he’ll","he’s","her","here","here’s",
        "hers","herself","him","himself","his","how","how’s","i","i’d","i’ll","i’m","i’ve","if","in","into","is","it",
        "it’s","its","itself","let’s","me","more","most","my","myself","nor","of","on","once","only",
        "or","other","ought","our","ours","ourselves","over","own","same","she","she’d","she’ll","she’s","should",
        "so","some","such","than","that","that’s","the","their","theirs","them","themselves","then","there","there’s",
        "these","they","they’d","they’ll","they’re","they’ve","this","those","through","to","too","under","until",
        "up","very","was","wasn't","we","we’d","we’ll","we’re","we’ve","were","what","what’s","when","when’s","where","where’s",
        "which","while","who","who’s","whom","why","why’s","with","would","you","you’d","you’ll","you’re","you’ve","your",
        "yours","yourself","yourselves"]

        #create a list of reviews with each line containing each review
        return_list = []
        for line in text :

            #split the reviews
            line = line.split("|")
            
            #line[0] and line[2] are of interest
            marker = line[0]
            text = line[2]
            text = text.lower()
            text = re.sub("[^A-Za-z']"," ",text)
            
            text = [word for word in text.split(" ") if (word not in stop_words) and (word != '')]
            to_append = [marker,text]
            return_list.append(to_append)

        return return_list

    def types_of_review(self,lines):

        review_type = Set()

        for line in lines:
            
            review_type.add(line[0])
            if(review_type.len()==2):
            
                break

        return review_type

    def train(self, lines):

        
        # lines = ['5|1|hello is anybody in there']
        #count the total number of reviews
        for line in lines:
          self.total_count+=1

        #set the total number of review type 1 and type 2
        processed_lines = self.text_process(lines)

        
        #create a function for review
        review_type = self.types_of_review(lines)
        list_of_markers = review_type.all_elements()
        
        #set the 2 types of reviews of this class
        self.review_type_1 = list_of_markers[0]
        self.review_type_2 = list_of_markers[1]
        


        for line in processed_lines:
    
            review = line[0]
            words = line[1]

            if review == self.review_type_1:
                self.total_type_1_review+=1

                for word in words :
                    if word not in self.type_1_word_list:
                        self.type_1_word_list[word]=1
                    else:
                        self.type_1_word_list[word]+=1 

            else :
                self.total_type_2_review+=1

                for word in words:
    
                    if word not in self.type_2_word_list:
                        self.type_2_word_list[word]=1
                    else:
                        self.type_2_word_list[word]+=1 



        #we have now got the word frequency according to review type
        self.prob_type_1 = (math.log(self.total_type_1_review / self.total_count))
        self.prob_type_2 = (math.log(self.total_type_2_review / self.total_count))

        for word in self.type_1_word_list :
            prob = math.log((1+self.type_1_word_list[word])/(self.total_type_1_review+2))
            self.type_1_word_list[word] = prob

        for word in self.type_2_word_list :
            prob = math.log((1+self.type_2_word_list[word])/(self.total_type_2_review+2))
            self.type_2_word_list[word] = prob

        self.add_one_smooth_type_1 = math.log(1/(self.total_type_1_review+2))
        self.add_one_smooth_type_2 = math.log(1/(self.total_type_2_review+2))



    def classify(self, lines):
        predictions = []
        probs =[]
        reviews_to_predict = self.text_process(lines)
        for review in reviews_to_predict:
            
            line = review[1]
            #create the probabilities for type 1 and type 2
            type_1_log_prob = 0.0
            type_2_log_prob = 0.0

            #calculate positive prob
            for word in line:

                #check if it is in positive freq word
                if word in self.type_1_word_list:
                    type_1_log_prob +=self.type_1_word_list[word]

                elif word in self.type_2_word_list:
                    type_1_log_prob += self.add_one_smooth_type_1

                if word in self.type_2_word_list:
                    type_2_log_prob +=self.type_2_word_list[word]
                elif word in self.type_1_word_list:
                    type_2_log_prob+=self.add_one_smooth_type_2

                    
            #add the prob of prior 
            type_1_log_prob+= self.prob_type_1
            type_2_log_prob+= self.prob_type_2

            #check which is greater then classify
            if type_1_log_prob >=type_2_log_prob:
                predictions.append(self.review_type_1)
                
            else :
                predictions.append(self.review_type_2)

        return predictions

