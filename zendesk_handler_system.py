import notifier
import time

def main():

    # begin loop
    while True:
        # pull recent tickets
        notifier.getZendeskTickets()
        # break up JSON response into list

        # check for encryption key reset requests

        # make new tickets accordingly

        # update Benzo Log Google Sheet
        print('Waiting 2 seconds')
        time.sleep(2)


main()