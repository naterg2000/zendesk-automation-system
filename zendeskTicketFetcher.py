# run this to get a csv of updated zendesk ticket data

# continue with this video: https://www.youtube.com/watch?v=3wC-SCdJK2c

import requests
import gspread
import re

# get ticket info from Zendesk
def getTickets(api_endpoint):

  # set the user parameters
  # to get a specific ticket: https://fyihelp.zendesk.com/api/v2/tickets/{ticke-id}
  # to get all recent tickets: 'https://fyihelp.zendesk.com/api/v2/tickets/recent'
  url = 'https://fyihelp.zendesk.com/api/v2/tickets/348'  # more recent benzo log with From field
  user="fyiintern001@gmail.com"
  pwd="Chocolate2020"

  # submit http request
  response = requests.get(url, auth=(user, pwd))

  # check for response codes other 200
  # if it's something other than 200, there was a problem
  # list possible response codes and what they mean
  if response.status_code != 200:
      print('Status:', response.status_code, 'Problem with the request. Exiting.')
      exit()
  
  # store repsonse as json
  data = response.json()
  print(data)

  # break up the json response into lists of data
  ticket_data = data[list(data.keys())[0]]  

  # save tickets in list for here
  extracted_data = list()
  
  # loop through each dataset
  # for each element in data
  for i in ticket_data:
    temp_ticket = list()

    # for each attribute in element
    temp_ticket.append(i['id'])
    temp_ticket.append(i['created_at'])
    temp_ticket.append(getTicketDescriptionAndPhoneNumber(i['description'])[0])
    temp_ticket.append(getTicketDescriptionAndPhoneNumber(i['description'])[1])
    temp_ticket.append(i['status'])

    # add the temp ticket data list to the list of tickets
    extracted_data.append(temp_ticket)
  
  return extracted_data



# get sender's phone number and report message 
# out of the ticket's description field
# returns user_phone_number AND  report_comment
def getTicketDescriptionAndPhoneNumber(ticket_description):
    
  # find text that matches the From: <phone number> pattern
  # ^ searches for the beginning of line, \+ seraches for the + character, [0-9] searches for a character between 0 and 9
  # * seraches for any amount of repeated characters between 0-9, $ searches for the end of the line (just before newline)
  phone_number_re = "^From:\+[0-9]*"  

  # find text that matches the report comment portion of an FYI report
  user_message_re = "\n[A-Za-z ’'!?.,()]+"

  # extract the phone number from the description
  # [0] because findall() returns a list and there is only one RE match, so we get the first list item
  user_phone_number = re.findall(phone_number_re, ticket_description)[0]  # extract the phone number from the description
  report_comment = re.findall(user_message_re, ticket_description)[0].replace('’', "'")

  return user_phone_number, report_comment



# write the new ticket data to the spreadsheet
def writeToSpreadsheet():
    
  sa = gspread.service_account(filename="fyi-zendesk-fetcher-f655e139dc89.json")
  ticketSheet = sa.open("Test Zendesk Data")

  wks = ticketSheet.worksheet("Sheet1") # this is the actual page within the Sheet
  return None

def main():
  
  getTickets("https://fyihelp.zendesk.com/api/v2/tickets/340")

  # writeToSpreadsheet()
  return None

main()
# set the user parameters
# to get a specific ticket: /api/v2/tickets/{ticket_id}
# to get all recent tickets: 'https://fyihelp.zendesk.com/api/v2/tickets/recent'
url = 'https://fyihelp.zendesk.com/api/v2/tickets/340'  # more recent benzo log with From field
user="fyiintern001@gmail.com"
pwd="Chocolate2020"

sa = gspread.service_account(filename="fyi-zendesk-fetcher-f655e139dc89.json")
ticketSheet = sa.open("Test Zendesk Data")

wks = ticketSheet.worksheet("Sheet1") # this is the actual page within the Google Sheet

# submit http request
response = requests.get(url, auth=(user, pwd))

# check for response codes other 200
# if it's something other than 200, there was a problem
# list possible response codes and what they mean
if response.status_code != 200:
    print('Status:', response.status_code, 'Problem with the request. Exiting.')
    exit()

# store response as json
data = response.json()
# print(data)

# a list of the data titles for the csv
extracted_ticket_data_titles = ["assignee id", "created at", "description", "id", "subject", "requester id", "updated at", "last updated by", "url", "submitted via"]

ticket_data = data[list(data.keys())[0]]  # store desired data from json response
num_tickets = 1
# print(ticket_data['description'])
getTicketDescription(ticket_data['description'])

info_to_extract = ["created_at", "description", "status"]
# print only specific data via loop
for i in range(0, num_tickets):
    this_ticket = list()
    for item in info_to_extract:
        this_ticket.append(ticket_data[item])
    # print(this_ticket)
    # wks.update('A1:C1', [this_ticket])  # pass ticket data as 2D array


# write the data to a csv file
# write = None
# extracted_ticket_data= None
# with open('ticket_data.csv', 'w') as f:
#   write = csv.writer(f) # using csv.writer method from CSV package
#   write.writerow(extracted_ticket_data_titles)  # write the header row fields


  # write the extracted ticket data to each row
  # for i in range(0, len(extracted_data_list)):
    # write.writerow(extracted_data_list[i])

    # to write to the spreadsheet
    # wks.update(<row range>, value)

# close file
# f.close()


# for more info: https://developer.zendesk.com/documentation/ticketing/getting-started/making-requests-to-the-zendesk-api/
# list of http response codes: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes