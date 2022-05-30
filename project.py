import nltk
nltk.download('stopwords')
import nltk
nltk.download('punkt')

from nltk.corpus import stopwords as sw
from nltk.tokenize import word_tokenize, sent_tokenize
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
from gensim.summarization.summarizer import summarize
from gensim.summarization.textcleaner import split_sentences
#from transformers import pipeline

def nltkSummary(yt):
    youtube_video=yt
    video_id = youtube_video.split("=")[1]
     
    #pass the video id in get_transcript function
    YouTubeTranscriptApi.get_transcript(video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
   
    #transcript has three parameters ->duration,start,text->we want text
    #result collects only 'text' from transcript
    result = ""
    for i in transcript:
        result += ' ' + i['text']
        
    
    #set allows only unique values
    stopwords = set (sw.words("english"))
    
    #tokenize the words in transcript
    words = word_tokenize(result)
    
    #take a dictionary to store each word [leaving the stopword] and its frequency
    freqTable = dict()
    for word in words:
        word=word.lower()
        if word in stopwords:
            continue
        if word in freqTable:
            freqTable[word]+=1
        else:
            freqTable[word]=1
       
    #now,tokenize sentences in transcript
    sentences = sent_tokenize(result)
    
    #CAT eats a rat
    #sentv[cat eats a rat]=1+1+1=3
    
    #create dictionary 
    sentenceValue = dict()
    for sentence in sentences:
        for word,freq in freqTable.items():
            if word in sentence.lower(): #ensures that the word under consideration is not a stopword
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq 
                   
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]
    
    average = int(sumValues / len(sentenceValue))
    summary = ' '
    for sentence in sentences:
        if(sentence in sentenceValue) and (sentenceValue[sentence] > (1.5 * average)):
            summary = summary+ " "+sentence      
    print("SUMMARY\n",summary)
    
    
def bartModel1(yt):
    youtube_video=yt
    video_id = youtube_video.split("=")[1]
    YouTubeTranscriptApi.get_transcript(video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
 

    result = ""
    for i in transcript:
        result += ' ' + i['text']
    #print(result)
    print(len(result))

    #Pass task and model in pipeline
    summarizer = pipeline('summarization' , model ="sshleifer/distilbart-cnn-6-6") 
    
    #create chunks of text
    #limit of 1 chunk is 1024 words
    num_iters = int(len(result)/1000)
    summarized_text = [] #to store summary from all chunks 
    for i in range(0, num_iters + 1):
      start = 0
      start = i * 1000  #start of chunk
      end = (i + 1) * 1000  #end of chunk
     # print("input text \n" + result[start:end])
      out = summarizer(result[start:end]) #pass result in summarizer
    
      
      out = out[0]
      out = out['summary_text']
      summarized_text.append(out)
    print("SUMMARY\n",summarized_text)
    
    
def bartModel2(yt):
    youtube_video=yt
    video_id = youtube_video.split("=")[1]
    YouTubeTranscriptApi.get_transcript(video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    result = ""
    for i in transcript:
        result += ' ' + i['text']
    #print(result)
    #print(len(result))

    summarizer = pipeline('summarization' , model ="facebook/bart-large-cnn") 
    num_iters = int(len(result)/1000)
    summarized_text = []
    
    for i in range(0, num_iters + 1):
      start = 0
      start = i * 1000
      end = (i + 1) * 1000
     # print("input text \n" + result[start:end])
      #minimum length 56 by default, maximum length is 142 by default
      out = summarizer(result[start:end], min_length=10,max_length=60)
      
      out = out[0]
      out = out['summary_text']
      #print("Summarized text\n"+out)
      summarized_text.append(out)

    print("SUMMARY\n",summarized_text)
    
        
def gensimSummary(yt):
    youtube_video=yt
    video_id = youtube_video.split("=")[1]
    YouTubeTranscriptApi.get_transcript(video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
  
    #obtain transcript of video
    result = ""
    for i in transcript:
        result += ' ' + i['text']
        

    def f(seq): # Order preserving unique sentences - sometimes duplicate sentences appear in summaries
        seen = set() #set to store unique sentences
        return [x for x in seq if x not in seen and not seen.add(x)]
   
    def summary(x, perc): #x input document, perc: percentage of the original document to keep
        if len(split_sentences(x)) > 10:
            test_summary = summarize(x, ratio = perc, split=True)
            test_summary = '\n'.join(map(str, f(test_summary))) #f is function
           
        else:
            test_summary = x #else the text is summary itself
        return test_summary
    

    # Get the Summary
    mysummary = summary(result, 0.5)
    print("SUMMARY\n",mysummary)
    
link=input("Enter youtube video link:")


while True:  
    print("\nMENU")  
    print("1.Get extarctive summary ")  
    print("2.Get abstractive summary")  
    print("3.Exit")  
    users_choice = int(input("\nEnter your Choice: "))  
  
# based on the users choice the relevant method is called
    if users_choice == 1: 
        while True:  
            print("\n1.Using Gensim model")  
            print("2.Using natrual language tootlkit")  
            print("3.Exit") 
            ch = int(input("\nEnter your Choice: ")) 
        
            if ch==1:
                gensimSummary(link)
                
            elif ch==2:
                nltkSummary(link)
                
            elif ch == 3:  
                break  
      
            else:  
                print("Please enter a valid Input from the list") 
            
          
    elif users_choice == 2:  
         while True:  
            print("\n1.Using sshleifer/distilbart-cnn-6-6 model")  
            print("2.Using facebook/bart-large-cnn ")  
            print("3.Exit") 
            ch = int(input("\nEnter your Choice: ")) 
        
            if ch==1:
                bartModel1(link)
                
            elif ch==2:
                bartModel2(link)
                
            elif ch == 3:  
                break  
      
            else:  
                print("Please enter a valid Input from the list") 

    elif users_choice == 3:  
         break  
      
    else:  
         print("Please enter a valid Input from the list") 
                
