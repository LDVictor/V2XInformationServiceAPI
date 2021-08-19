class RSUModel:
    def __init__(self, rsu_id, type, coord_x, coord_y):
        self.rsu_id = rsu_id
        self.type = type
        self.coord_x = coord_x
        self.coord_y = coord_y

    def json(self):
        return {
            'rsu_id': self.rsu_id,
            'type': self.type,
            'coord_x': self.coord_x,
            'coord_y': self.coord_y
        }
