class StationStats:
    __slots__=("min","max","avarage","count")
    def __init__(self,value:int) -> None:
        self.min=value
        self.max=value
        self.avarage=value
        self.count=1
    def update(self,value:int):
        if value < self.min:
            self.min = value
        if value > self.max:
            self.max = value
        self.avarage += value
        self.count += 1
    def merge(self,other:"StationStats"):
        if other.min < self.min:
            self.min = other.min
        if other.max > self.max:
            self.max = other.max
        self.avarage += other.avarage
        self.count += other.count
    def __repr__(self) -> str:
        return f"{self.min/10};{round(self.avarage/self.count/10,1)};{self.max/10}"