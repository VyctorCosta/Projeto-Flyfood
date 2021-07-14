import math, random, time
def setRandomSeed(seed):
    if seed:
        random.seed(seed)
    else:
        seed=time.time()
    return seed
    
def distance2Points(Point1, Point2, distance_type):
    if distance_type == 'EUC_2D':
        xd = Point1.x - Point2.x
        yd = Point1.y - Point2.y
        dij = int(math.sqrt(xd*xd + yd*yd))
        return dij

    elif distance_type == 'GEO':
        pi = 3.141592
        deg = int(Point1.x)
        min = Point1.x - deg
        latitude_i = pi * (deg + 5.0 * min / 3.0) / 180.0
        deg = int(Point1.y)
        min = Point1.y - deg
        longitude_i = pi * (deg + 5.0 * min / 3.0) / 180.0
        deg = int(Point2.x)
        min = Point2.x - deg
        latitude_j = pi * (deg + 5.0 * min / 3.0) / 180.0
        deg = int(Point2.y)
        min = Point2.y - deg
        longitude_j = pi * (deg + 5.0 * min / 3.0) / 180.0
        rrr = 6378.388
        q1 = math.cos(longitude_i - longitude_j)
        q2 = math.cos(latitude_i - latitude_j)
        q3 = math.cos(latitude_i + latitude_j)
        dij = int(rrr * math.acos( 0.5 * ((1.0+q1)*q2 - (1.0-q1)*q3)) + 1.0)
        return dij

def distanceNPoints(list, distance_type='EUC_2D'):
    list_aux = list.copy()
    point_j = list_aux.pop(0)
    distance = 0
    for point_i in list_aux:
        distance += distance2Points(point_j, point_i, distance_type)
        point_j = point_i
    return distance

def selectParents(list_individuals, type):
    if type.lower() == 'roleta':
        total = 0
        value = 0
        for i in list_individuals:
            total += i.returnFitness()
        check = random.random()
        for i in list_individuals:
            if value <= check <= value + (i.returnFitness() / total):
                return i
            value += i.returnFitness() / total
    elif type.lower() == 'torneio':
        candidate_one = random.choice(list_individuals)
        candidate_two = random.choice(list_individuals)
        while candidate_two == candidate_one:
            candidate_two = random.choice(list_individuals)
        if candidate_one.returnDistance() < candidate_two.returnDistance():
            return candidate_one
        return candidate_two

def CrossingOver(father, mother):
    cut = random.randint(1, len(father)-1)
    son1 = father[:cut]
    list_aux = mother.copy()
    for i_f,v_f in enumerate(son1):
        for i_m,v_m in enumerate(list_aux):
            if v_m == v_f:
                backup = list_aux[i_f]
                list_aux[i_f] = list_aux[i_m]
                list_aux[i_m] = backup
                break
    son1 += list_aux[cut:]
    son2 = mother[:cut]
    list_aux = father.copy()
    for i_m,v_m in enumerate(son2):
        for i_f,v_f in enumerate(list_aux):
            if v_f == v_m:
                backup = list_aux[i_f]
                list_aux[i_f] = list_aux[i_m]
                list_aux[i_m] = backup
    son2 += list_aux[cut:]
    return (son1, son2)

def Mutation(list):
    for i in list:
        chance = random.random()
        if chance <= 0.01:
            i = random.randint(0, len(list)-1)
            j = random.randint(0, len(list)-1)            
            while j == i:
                j = random.randint(0, len(list)-1)            
            aux = list[j]
            list[j] = list[i]
            list[i] = aux

def Partition(Arranjo, p, r):
    x = Arranjo[r].returnDistance()
    i = p - 1
    for j in range(p, r):
        if Arranjo[j].returnDistance() <= x:
            i += 1
            backup = Arranjo[i]
            Arranjo[i] = Arranjo[j]
            Arranjo[j] = backup
    backup = Arranjo[i+1]
    Arranjo[i+1] = Arranjo[r]
    Arranjo[r] = backup
    return i+1

def QuickSort(Arranjo, p, r):
    if p < r:
        q = Partition(Arranjo, p, r)
        QuickSort(Arranjo, p, q-1)
        QuickSort(Arranjo, q+1, r)

class GA():
    def __init__(self, num_individuals, coords):
        self.coords = coords
        self.__num_individuals = num_individuals
        self.__list_individuals = [route(coords) for i in range(num_individuals)]
        self.__best_individual = self.__list_individuals[0]
    
    def crossing_population(self, type):
        children_population = []
        for i in range(int(len(self.__list_individuals)//2)):
            father = selectParents(self.__list_individuals, type)
            mother = selectParents(self.__list_individuals, type)
            while mother == father:
                mother = selectParents(self.__list_individuals, type)
            chance = random.random()
            if chance <= 0.7:
                son1, son2 = CrossingOver(father.returnList(), mother.returnList())
                Mutation(son1)
                Mutation(son2)
                son1 = route(self.coords, son1)
                son2 = route(self.coords, son2)
                children_population.append(son1)
                children_population.append(son2)
            else:
                son1 = father.returnList().copy()
                son2 = father.returnList().copy()
                Mutation(son1)
                Mutation(son2)
                son1 = route(self.coords, son1)
                son2 = route(self.coords, son2)
                children_population.append(son1)
                children_population.append(son2)
        self.__list_individuals.extend(children_population)

    def selectBestIndividuals(self, elitism, num=None):
        if elitism:
            if num == None:
                num = 1
            aux = []
            for i in range(num):
                aux.append(self.__list_individuals.pop(0))
            QuickSort(self.__list_individuals, 0, len(self.__list_individuals)-1)
            while len(self.__list_individuals) != self.__num_individuals - len(aux):
                self.__list_individuals.pop(-1)
            for i in aux:
                if i.returnDistance() < self.__list_individuals[0].returnDistance():
                    self.__list_individuals.insert(0, i)
                else:
                    self.__list_individuals.append(i)
        else:
            QuickSort(self.__list_individuals, 0, len(self.__list_individuals)-1)
            aux = self.__list_individuals[:int(len(self.__list_individuals)//2)]
            self.__list_individuals = aux
        self.__best_individual = self.__list_individuals[0]

    def setFitness(self):
        total = 0
        for i in self.__list_individuals:
            total += i.returnDistance()
        for i in self.__list_individuals:
            i.setFitness(math.cos((i.returnDistance() / total) * math.pi / 2))

    def returnBestIndividual(self):
        return self.__best_individual

    def returnWorseIndividual(self):
        return self.__list_individuals[-1]

    def returnAvarageIndividuals(self):
        dis = 0
        for i in self.__list_individuals:
            dis += i.returnDistance()
        return dis/self.__num_individuals

class route():
    def __init__(self, coords,list=None):
        if not list:
            self.__list = [i for i in coords]
            random.shuffle(self.__list)
            self.__route = [city(i, coords[i]) for i in self.__list]
        else:
            self.__list = list
            self.__route = [city(i, coords[i]) for i in list]
        self.coords = coords
        self.calculeDistance()
        self.__fitness = None

    def changeRoute(self, list):
        self.__route = [city(i, self.coords[i]) for i in list]

    def calculeDistance(self):
        self.__distance = distanceNPoints(self.__route)
    
    def setFitness(self, fitness):
        self.__fitness = fitness
    
    def returnFitness(self):
        return self.__fitness
    
    def returnDistance(self):
        return self.__distance

    def returnRoute(self):
        return self.__route

    def returnList(self):
        return self.__list

class city():
    def __init__(self, num, coords):
        self.num = num
        self.x = coords[0]
        self.y = coords[1]

