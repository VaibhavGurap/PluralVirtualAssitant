from shareplum import Site, Office365
from shareplum.site import Version
import pandas as pd


USERNAME="vaibhav.gurap@pluraltechnology.com"
PASSWORD="Muw50953"
SHAREPOINT_URL="https://pluraltechnologypvtltd.sharepoint.com/"
SHAREPOINT_SITE="https://pluraltechnologypvtltd.sharepoint.com/sites/Test-assitant"

class SharePoint:
    def auth(self):
        self.authcookie = Office365(
            SHAREPOINT_URL,
            username=USERNAME,
            password=PASSWORD,
        ).GetCookies()
        self.site = Site(
            SHAREPOINT_SITE,
            version=Version.v365,
            authcookie=self.authcookie,
        )
        return self.site

    def connect_to_list(self, ls_name):
        self.auth_site = self.auth()

        list_data = self.auth_site.List(list_name=ls_name).GetListItems()

        return list_data
    

def getMeeting(email:str):
    meetings = SharePoint().connect_to_list(ls_name='meetings')
    df = pd.DataFrame(meetings)
    df['MeetingStartTime'] = pd.to_datetime(df['MeetingStartTime']).dt.tz_localize('America/Los_Angeles').dt.tz_convert('Asia/Kolkata')
    df['MeetingEndTime'] = pd.to_datetime(df['MeetingEndTime']).dt.tz_localize('America/Los_Angeles').dt.tz_convert('Asia/Kolkata')
    print(df[['MeetingStartTime','MeetingEndTime']])
    today_df = df[df['MeetingStartTime'].dt.date == pd.Timestamp.today().date()]
    print(today_df[['MeetingStartTime']])
    today_df['MeetingWith']=today_df['MeetingWith'].fillna('')
    filtered_df=today_df[today_df['MeetingWith'].str.contains(email+";",case=False)]
    return filtered_df

def checkAppointment(email:str):
    meeting=getMeeting(email)
    if len(meeting)>0:
        print("Organizer: "+meeting["Organizer"])
        print("Meeting Id: "+meeting['MeetingId'])
        print("Meeting Subject: "+meeting["MeetingSubject"].astype(str))
        return (True,meeting)
    else:
        return (False,)

    