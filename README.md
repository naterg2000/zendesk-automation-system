# zendesk-automation-system

```pip install requests```<br>
```pip install gspread```<br>
```pip install pyqt5```<br>

<p>This is an automation system for the FYI team. The system looks at any unsolved tickets and checks the subject to see if they are requests to reset the user's Encryption Key and also whether that user has been replied to or not.
If not, a Zendesk Ticket is automatically created in response to this request. The original request ticket is merged into the newly made response ticket.</p>

<br>

<p>Upcoming Things:</p><br>
<ul>
  <li>UI for the Ssystem.</li>
  <li>Debugging Mode: will refrain from making tickets and sending emails.</li>
  <li>Benzo Log Updater: automatically add Benzo Log reports to our Google Sheet for tracking.</li>
  <li>More stability/anti-crash functionality.</li>
</ul>
