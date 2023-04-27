class GPSDate:
    def __init__(self, date):
        self.date = date
        self.gps_times = {}
    
    def add_gps_time(self, time, x_coord, y_coord):
        self.gps_times[time] = {'long': x_coord, 'lat': y_coord}
        
    def __str__(self):
        return f'{self.date}: {self.gps_times}'