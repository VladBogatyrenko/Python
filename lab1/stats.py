class StationStats:
    __slots__=("_min","_max","_avarage","_count")
    def __init__(self,value:int) -> None:
        self._min=value
        self._max=value
        self._avarage=value
        self._count=1
    def update(self,value:int)->None:
        if value < self._min:
            self._min = value
        if value > self._max:
            self._max = value
        self._avarage += value
        self._count += 1
    def merge(self,other:"StationStats")->None:
        if other._min < self._min:
            self._min = other._min
        if other._max > self._max:
            self._max = other._max
        self._avarage += other._avarage
        self._count += other._count
    def __repr__(self) -> str:
        return f"{self._min/10};{round(self._avarage/self._count/10,1)};{self._max/10}"

    @property
    def min(self)->float:
        return self._min/10

    @property
    def max(self) -> float:
        return self._max/10

    @property
    def avarage(self) -> float:
        return round(self._avarage/self._count/10,1)