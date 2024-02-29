from datetime import datetime, timedelta

class Date:
    def __init__(
        self, 
        year = datetime.now().year,
        month = datetime.now().month, 
        day = datetime.now().day
    ) -> None:
        self.date = datetime(year, month, day)

    def get_earlier(self, days_earlier):
        return self.date - timedelta(days=days_earlier)
    
    def get_later(self, days_later):
        return self.date + timedelta(days=days_later)
    
    def get_date(self):
        return self.date