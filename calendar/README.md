# calendar-furiere

Use a cronjob to check events retrieved from a calendar API. If it's time it triggers an event.


### About Google Calendar API implementation
Without knowing the full list of requirements for the complete application, I can note only that authentication of users is required
in the actual implementation. Even passing a secret token in the `Authorization` header instead of the email, the service would still lack of SSL. 
* Google Calendar API would make everything safe using a secure connection and federated login from/to clients
* It would allow to delete events and calendars
* It would let the authorized clients to store/watch changes in user activities 
* It would add some features like moving events among calendars
* It would give integration with a mail server to send notifications.

In general the architecture could provide linked resources to Calendar's events, The client could fetch aggregated data from
the local architecture (like a list of Calendar's id for a particular users, with particular characteristics) and then fetch the complete objects from Calendar.
Or it could use Calendar as 'history', allowing the local architecture to serve only event to-be with a great saving in terms
of memory used. Once some kind of aggregated data is needed for a particular user, the app can ask the 'history' from Google's service.