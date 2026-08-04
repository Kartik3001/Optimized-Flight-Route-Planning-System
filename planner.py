from flight import Flight

class Queue:
    def __init__(self):
        self.queue = []
        self.size = 0
    
    def enqueue(self, item):
        self.queue.append(item)
        self.size += 1
    
    def dequeue(self):
        if self.size == 0:
            return None
        else:
            self.size -= 1
            return self.queue.pop(0)
    
    def is_empty(self):
        return self.size == 0
    
    def __len__(self):
        return self.size
    

'''
Python Code to implement a heap with general comparison function
'''

class Heap:
    '''
    Class to implement a heap with general comparison function
    '''
    
    def __init__(self, comparison_function, init_array):
        '''
        Arguments:
            comparison_function : function : A function that takes in two arguments and returns a boolean value
            init_array : List[Any] : The initial array to be inserted into the heap
        Returns:
            None
        Description:
            Initializes a heap with a comparison function
            Details of Comparison Function:
                The comparison function should take in two arguments and return a boolean value
                If the comparison function returns True, it means that the first argument is to be considered smaller than the second argument
                If the comparison function returns False, it means that the first argument is to be considered greater than or equal to the second argument
        Time Complexity:
            O(n) where n is the number of elements in init_array
        '''
        
        # Write your code here
        self.compare = comparison_function
        self.heap = init_array
        len_heap = len(self.heap)
        if len_heap!=0:
            for i in range(len_heap//2-1,-1,-1):
                self._heap_down(i)
        pass
        
    def insert(self, value):
        '''
        Arguments:
            value : Any : The value to be inserted into the heap
        Returns:
            None
        Description:
            Inserts a value into the heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        # Write your code here
        self.heap.append(value)
        self._heap_up(len(self.heap)-1)
        pass
    
    def extract(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value extracted from the top of heap
        Description:
            Extracts the value from the top of heap, i.e. removes it from heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        # Write your code here
        if len(self.heap)==0:
            return None
        if len(self.heap)==1:
            return self.heap.pop()
        top_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heap_down(0)
        return top_val
        pass
    
    def top(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value at the top of heap
        Description:
            Returns the value at the top of heap
        Time Complexity:
            O(1)
        '''
        
        # Write your code here
        if len(self.heap)==0:
            return None
        return self.heap[0]
        pass
    
    # You can add more functions if you want to
    def _heap_up(self, i):
        while i>0:
            parent = (i-1)//2
            if self.compare(self.heap[i], self.heap[parent]):
                self.heap[i],self.heap[parent] = self.heap[parent],self.heap[i]
                i = parent
            else:
                break
    
    def _heap_down(self, i):
        while 2*i+1<len(self.heap):
            left_child = 2*i+1
            right_child = 2*i+2
            if right_child<len(self.heap) and self.compare(self.heap[right_child],self.heap[left_child]):
                min_child = right_child
            else:
                min_child = left_child
            if self.compare(self.heap[min_child],self.heap[i]):
                self.heap[i],self.heap[min_child] = self.heap[min_child],self.heap[i]
                i = min_child
            else:
                break

    def __len__(self):
        return len(self.heap)



class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        self.flights = flights
        self.no_flights = len(flights) + 1
        self.m = max(max(i.start_city, i.end_city) for i in self.flights) + 1
        self.all_flights = [[] for i in range(self.m)]
        for i in self.flights:
            self.all_flights[i.start_city].append(i)

        self.possible_flights = [[] for i in range(self.no_flights)]
        for i in self.flights:
            for j in self.all_flights[i.end_city]:
                if j.departure_time - i.arrival_time >= 20:
                    self.possible_flights[i.flight_no].append(j)
        pass
        
    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        arrives the earliest
        """
        if start_city == end_city:
            return []
        visited = [float('inf') for i in range(self.no_flights)]

        queue = Queue()
        best_path = []
        
        best_arrival_time = float('inf')
        max_depth = float('inf')
        
        for i in self.all_flights[start_city]:
            if i.departure_time >= t1 and i.arrival_time <= t2:
                visited[i.flight_no] = i.arrival_time
                queue.enqueue((i, None, 0))
        
        while not queue.is_empty():
            flight, parent, depth = queue.dequeue()
            if depth > max_depth:
                break
            if flight.end_city == end_city and flight.arrival_time <= t2:

                if flight.arrival_time < best_arrival_time or depth < max_depth:
                    best_arrival_time = flight.arrival_time
                    best_path = []
                    while parent is not None:
                        
                        best_path.append(flight)
                        flight = parent[0]
                        parent = parent[1]
                    best_path.append(flight)
                    # if len(new_best_path) <= len(best_path) or best_path == []:
                    #     best_path = new_best_path
                    #     best_arrival_time = flight.arrival_time
                max_depth = depth
            
            # if depth > max_depth:
            #     break

            for i in self.possible_flights[flight.flight_no]:
                if i.arrival_time <= t2 and visited[i.flight_no] > i.arrival_time:
                    visited[i.flight_no] = i.arrival_time
                    queue.enqueue((i, (flight, parent, depth), depth+1))
        best_path.reverse()
        return best_path                        
                
        pass
    


    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """
        if start_city == end_city:
            return []
        
        
        visited = [False for i in range(self.no_flights)]
        
        best_cost = float('inf')
        best_path = []

        flights_heap = Heap(lambda x, y: x[0] < y[0], [])
            
        # starting_flights = []
        for i in self.all_flights[start_city]:
            
            if i.departure_time >= t1 and i.arrival_time <= t2:

                visited[i.flight_no] = True
                # starting_flights.append((i.fare, i, None))
                flights_heap.insert((i.fare, i, None))
                
        # heaps = Heap(lambda x, y: x[0] < y[0], starting_flights)
        
        while len(flights_heap) > 0:
            
            cost, arriving_flight, parent = flights_heap.extract()
            # print(cost, arriving_flight.flight_no, parent)
            if visited[arriving_flight.flight_no] and parent is not None:
                continue

            if arriving_flight.end_city == end_city:
                if cost < best_cost or best_path == []:
                    best_cost = cost
                    best_path = []
                    while parent is not None:
                        best_path.append(arriving_flight)
                        
                        arriving_flight = parent[1]
                        parent = parent[2]

                    best_path.append(arriving_flight)
                    break
                    

            for j in self.possible_flights[arriving_flight.flight_no]:
                if j.arrival_time <= t2 and not visited[j.flight_no]:
                    flights_heap.insert((cost + j.fare, j, (cost, arriving_flight, parent)))
            
            visited[arriving_flight.flight_no] = True

        

        best_path.reverse()
        return best_path

        pass
    


    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """

        if start_city == end_city:
            return []
        
        visited = [float('inf') for i in range(self.no_flights)]
        queue = Queue()
        
        best_cost = float('inf')
        max_depth = float('inf')
        best_path = []

        for i in self.all_flights[start_city]:
            if i.departure_time >= t1 and i.arrival_time <= t2:
                visited[i.flight_no] = i.fare
                queue.enqueue((i, None, 0, i.fare))
        
        while not queue.is_empty():
            flight, parent, depth, cost = queue.dequeue()
            if depth > max_depth:
                break
            if flight.end_city == end_city and flight.arrival_time <= t2:
                if cost < best_cost and depth <= max_depth:
                    best_cost = cost
                    best_path = []
                    max_depth = depth
                    while parent is not None:
                        best_path.append(flight)
                        flight = parent[0]
                        parent = parent[1]
                    best_path.append(flight)
                
                
            for i in self.possible_flights[flight.flight_no]:
                if i.arrival_time <= t2 and visited[i.flight_no] > cost + i.fare:
                    visited[i.flight_no] = cost + i.fare
                    new_cost = cost + i.fare
                    queue.enqueue((i, (flight, parent, depth, cost), depth+1, new_cost))
        
        best_path.reverse()
        return best_path  
        pass