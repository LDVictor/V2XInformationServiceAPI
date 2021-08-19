class VehicleModel:
    def __init__(self, vehicle_id, type, max_speed, coord_x, coord_y):
        self.vehicle_id = vehicle_id
        self.type = type
        self.max_speed = max_speed
        self.coord_x = coord_x
        self.coord_y = coord_y

    def json(self):
        return {
            'vehicle_id': self.vehicle_id,
            'type': self.type,
            'max_speed': self.max_speed,
            'coord_x': self.coord_x,
            'coord_y': self.coord_y
        }
