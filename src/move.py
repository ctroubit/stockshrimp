class Move:

    def __init__(self, inital, final):
        self.inital = inital
        self.final = final

    def __str__(self):
        return f'{self.inital.row},{self.inital.col} -> {self.final.row},{self.final.col}'
    
    def __eq__(self, value):
        return self.inital == value.inital and self.final == value.final