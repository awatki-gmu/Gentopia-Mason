from typing import AnyStr
from gentopia.tools.basetool import *
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

class GetCalendarEventsArgs(BaseModel):
    query: str = Field(..., description="a search query for scheduled events in Google Calendar")
    
class GetCalendarEvents(BaseTool):
    """Tool that adds the capability to query the Google Calendar API."""

    name = "google_calendar"
    description = ("A tool to return Google Calendar events."
                   "Input should be a query about the events in the calendar.")

    args_schema: Optional[Type[BaseModel]] = GetCalendarEventsArgs

    def _run(self, query: AnyStr) -> str:
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
        creds = service_account.Credentials.from_service_account_file("cs-678-hw2-fe00ad3b39d8.json", scopes=SCOPES)
        
        try:
            service = build("calendar", "v3", credentials=creds)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
            events_result = (
                service.events()
                .list(
                    calendarId="alexandrawatkins4@gmail.com",
                    timeMin=now,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])
            return str(events)
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error


    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = GetCalendarEvents()._run("What's the next upcoming event on my Google Calendar?")
    print(ans)
