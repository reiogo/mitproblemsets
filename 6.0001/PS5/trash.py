import string
from datetime import datetime
import pytz


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
        # # Join the list together.
        # checked_text = ''
        # checked_text = ' '.join(text_tmp_)
        # Split phrase and check each, check that they are consecutive.
        phrase_split = self.phrase.split()
        checker = ''
        if phrase_split[0] in text_tmp:
            phrase_index = text_tmp.index(phrase_split[0])
            for t in range(len(phrase_split)):
                if len(text_tmp) >= ((phrase_index + 1) + t):
                    checker += text_tmp[phrase_index + (t)] + ' '
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
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        if self.is_phrase_in(story.get_title()):
            return True
        else:
            return False

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


class BeforeTrigger(TimeTrigger):
    def __init__(self, time):
        TimeTrigger.__init__(self, time)
    def evaluate(self, story):
        '''
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        '''
        if self.get_time() > story:
            return True
        else:
            return False

class NotTrigger(Trigger):
    def __init__(self, phrase):
        self.other_trigger = PhraseTrigger(phrase)

    def get_other_trigger(self):
        return self.other_trigger

    def evaluate(self, story):
        return not self.other_trigger.evaluate(story.get_description())



if __name__ =='__main__':
    
    cuddly    = NewsStory('', 'hello, this is the neationl The@Purple!', '', '', datetime.now())
    test = NotTrigger('seven')
    print(test.evaluate(cuddly))
    



    def line_reader(line):
        data = line.split(',')
        if data[0] != "ADD":
            if data[1] == "OR" or data[1] == "AND":
                trigger_dict[data[0]] = t_map[data[1]](trigger_dict[data[2]],
                        trigger_dict[data[3]])
            else:
                trigger_dict[data[0]] = t_map[data[1]](data[2])
        else: 
            trigger_list[:] += [trigger_dict[t] for t in data[1:]]

    for line in lines:
        line_reader(line)
    print("trigger_list", trigger_list)
    print("trigger_dict: ", trigger_dict)

    return trigger_list

-------------------------------------------
    # For all lines.
    for m in lines:
        # Define data from lines.
        data = m.split(',')
        print("data: ", data)
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
                name = str(data[0])
                name = trigger_map[data[1]](data[2])
                trigger_dict[data[0]] = name

                # trigger_dict[data[0]] = trigger_map[data[1]](data[2])
        else:
            for t in data[1:]:
                trigger_list.append(trigger_dict.get(t))
    print("trigger_list: ", trigger_list)
    print("trigger_dict: ", trigger_dict)
    return trigger_list

    print(lines) # for now, print it so you see what it contains!

