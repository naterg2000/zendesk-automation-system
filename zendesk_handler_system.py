import notifier
import time

def main():

    # store login info
    login_credentials = notifier.getLoginInfo()

    # begin loop
    while True:
        # pull recent tickets
        email_list = notifier.getZendeskTickets(login_credentials)

        print('email list has', len(email_list), 'emails')

        # make new tickets accordingly

        # update Benzo Log Google Sheet
        print('Waiting 2 seconds')
        time.sleep(2)
        

main()