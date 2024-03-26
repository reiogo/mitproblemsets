# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Ray O
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    '''
    Initialize a NewsStory object

    guid (string): globally unique identifier

    title (string): title

    description (string): description

    link(string): url

    pubdate (int?): datetime, date published

    A NewsStory has 5 attributes
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    '''
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate


    def get_guid(self):
        return self.guid


    def get_title(self):
        return self.title


    def get_description(self):
        return self.description


    def get_link(self):
        return self.link


    def get_pubdate(self):
        return self.pubdate




#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        '''
         Initialize PhraseTrigger

         phrase (string): trigger phrase
         
         a PhraseTrigger object has one attribute
            self.phrase
        '''
        # Make phrase not case sensitive 
        self.phrase = phrase.lower()


    def get_phrase(self):
       '''
       Used to safely acces checked_text
       '''
       return self.phrase


    def is_phrase_in(self, text):
        '''
        Takes text (str arg)(not case sensitive).

        Returns True if whole phrase is in text.

        Returns False otherwise.
        '''
        # Initiate copy of checked_text to not mutate original.
        text_copy = text[:]
        text_copy = text_copy.lower()
        # Replace all punctuation with spaces.
        for char in string.punctuation:
            text_copy = text_copy.replace(char, ' ')
        text_copy = text_copy.split(' ')
        # # Make a list without the spaces.
        text_tmp = []
        for m in range(len(text_copy)):
            if text_copy[m] != '':
                text_tmp.append(text_copy[m])
        # Split phrase.
        phrase_split = self.phrase.split()
        # Initiate checker variable.
        checker = ''
        # If the first word of the phrase is in the text.
        if phrase_split[0] in text_tmp:
            # Get the index of the word.
            phrase_index = text_tmp.index(phrase_split[0])
            # loop over the length of the phrase to add words to the checker.
            for t in range(len(phrase_split)):
                # Prevent indexing from going out of range.
                if len(text_tmp) >= ((phrase_index + 1) + t):
                    checker += text_tmp[phrase_index + (t)] + ' '
        # Check if the checker(without the trailing whitespace) matches the phrase.
        if checker[:-1] == self.phrase:
            return True
        else:
            return False


    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        if self.is_phrase_in(story):
            return True
        else:
            return False


# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        '''
         Initialize TitleTrigger

         phrase (string): trigger phrase
         
         a TitleTrigger object has one attribute
            self.phrase
        '''
        PhraseTrigger.__init__(self, phrase)
    

    
    def evaluate(self, story):
        '''
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        '''
        if self.is_phrase_in(story.get_title()):
            return True
        else:
            return False


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        '''
         Initialize DescriptionTrigger

         phrase (string): trigger phrase
         
         a DescriptionTrigger object has one attribute
            self.phrase
        '''
        PhraseTrigger.__init__(self, phrase)
    

    
    def evaluate(self, story):
        '''
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        '''
        if self.is_phrase_in(story.get_description()):
            return True
        else:
            return False
        

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    def __init__(self, time):
        '''
        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
        Convert time from string to a datetime before saving it as an attribute.
        '''
        formatted_time = datetime.strptime(time,"%d %b %Y %H:%M:%S")
        formatted_time = formatted_time.replace(tzinfo=pytz.timezone("EST"))
        self.time = formatted_time


    def get_time(self):
        return self.time
    

# Problem 6
class BeforeTrigger(TimeTrigger):
    def __init__(self, time):
        TimeTrigger.__init__(self, time)
        
            
    def evaluate(self, story):
        '''
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        '''
        try:
            if self.get_time() > story.get_pubdate():
                return True
            else:
                return False
        except TypeError:
            tmp_time = self.get_time()
            tmp_time = tmp_time.replace(tzinfo= None)
            if tmp_time > story.get_pubdate():
                return True
            else:
                return False



class AfterTrigger(TimeTrigger):
    def __init__(self, time):
        TimeTrigger.__init__(self, time)


    def evaluate(self, story):
        '''
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        '''
        try:
            if self.get_time() < story.get_pubdate():
                return True
            else:
                return False
        except TypeError:
            tmp_time = self.get_time()
            tmp_time = tmp_time.replace(tzinfo= None)
            if tmp_time  < story.get_pubdate():
                return True
            else:
                return False


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, other_trigger):
        self.other_trigger = other_trigger


    def evaluate(self, x):
        # x is the news item.
        return not self.other_trigger.evaluate(x)


# Problem 8
class AndTrigger(Trigger):
    def __init__(self, trigger_one, trigger_two):
        self.trigger_one = trigger_one
        self.trigger_two = trigger_two


    def evaluate(self, x):
        # x is the news item.
        return (self.trigger_one.evaluate(x)
                and self.trigger_two.evaluate(x))


# Problem 9
class OrTrigger(Trigger):
    def __init__(self, trigger_one, trigger_two):
        self.trigger_one = trigger_one
        self.trigger_two = trigger_two


    def evaluate(self, x):
        # x is the news item.
        return (self.trigger_one.evaluate(x)
                or self.trigger_two.evaluate(x))


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    res = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                res.append(story)
    return  res



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    trigger_map = {"TITLE": TitleTrigger,
            "DESCRIPTION": DescriptionTrigger,
            "AFTER": AfterTrigger,
            "BEFORE": BeforeTrigger,
            "NOT": NotTrigger,
            "AND": AndTrigger,
            "OR": OrTrigger
             }

    trigger_dict = {}
    trigger_list = []
    

    # For all lines.
    for m in lines:
        # Define data from lines.
        data = m.split(',')
        # If first in the list is not  an ADD then:
        if data[0] != "ADD":
            # If second is an OR or AND then: define trigger_dict key and value.
            if data[1] == "OR" or data[1] == "AND":
                # Key is t number value.
                # Value is trigger with the two subjects.
                trigger_dict[data[0]] = trigger_map[data[1]](trigger_dict[data[2]],
                                        trigger_dict[data[3]])
            else:
                # Key is t number.
                # Value is  trigger with data[2] as element.
                trigger_dict[data[0]] = trigger_map[data[1]](data[2])
        else:
            for t in data[1:]:
                trigger_list.append(trigger_dict.get(t))
    return trigger_list



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("Trump")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("AI")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
