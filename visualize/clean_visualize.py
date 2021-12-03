import csv
import re
text_file = open("message.txt", "wt")
location_dic = {}
#location_file = open('location.txt',"wt")
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
with open('tweet_output.csv',newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if (row[1] == 'message'):
            continue
        else:
            #print(row[1]) #message
            temp_mess = row[1]
            temp_clean_mess = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', temp_mess, flags=re.MULTILINE)#clean link
            temp_clean_mess = emoji_pattern.sub(r'', temp_clean_mess)#clean emoji
            n = text_file.write(temp_clean_mess)
            temp_clean_location = row[9]
            if temp_clean_location in location_dic.keys():
                original_count = location_dic[temp_clean_location]+1
                location_dic.update({temp_clean_location:original_count})
            else:
                location_dic[temp_clean_location]=1
            
            #print(temp_clean_mess)
text_file.close()
sortted_loaction = sorted(location_dic.items(), key=lambda x: x[1], reverse=True)
print(sortted_loaction[:50])
#location_file.close()
with open('location_frequency.csv', mode='w') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    employee_writer.writerow(['Location Name', 'Frequency'])
    for item in sortted_loaction:
        employee_writer.writerow([item[0],item[1]])