import sys
from expand import expand
import heapq

def a_star_search (dis_map, time_map, start, end):
	path = []
	# TODO Put your code here.
	# be sure to call the imported function expand to get the next list of nodes

	#Time taken to reach each node
	time_taken_for_each_node = {}
	time_taken_for_each_node[start] =0

	#Inititalize an empty visited set - 
	visited =set()
	#Initialize the priority queue by adding the start element to the queue with weight zero
	priority_queue = PriorityQueue()
	priority_queue.add_node([start],0)



	#Check if the start and end is not in the time map then return the path
	if start not in time_map and end not in time_map:
		return path

	#Check if the start and end is not in the dis map
	if start not in dis_map and end not in dis_map:
		return path
	
	#Check if the start is in the time map and end not in dis map
	if start in time_map and end not in dis_map:
		return path
	#Check if the end is in the time map but not in dis map
	if end in time_map and start not in dis_map:
		return path

	#Check if the keys are present in all
	if dis_map.keys() != time_map.keys():
		return path


	#Nodes added
	# #If queue is not empty run a loop and keep popping node
	while priority_queue.empty() == False :


		#pop the element and add it to the set of visited along with the time
		current_node_tuple = priority_queue.pop_node()
		# current_node = current_node_tuple[0]
		# print("CURRENT NODE : ".format(current_node_tuple[1]))

		#Check if the node has already been visited if not then add to visited
		if current_node_tuple[1][-1] not in visited:
			visited.add(current_node_tuple[1][-1])

			#check if the current is the destination if yes then return
			if current_node_tuple[1][-1] == end :
				path = current_node_tuple[1]
				# print("Found the path")
				return path

			#Else get all the neighbors of current node from expand
			#Push onto the heap using heuristics of distance
			for node in expand(current_node_tuple[1][-1],time_map):
				# print("Node {} in {} ".format(node,current_node_tuple[1][-1]))
				# print("")
				#Get the cost of going to the node 
				time_cost = time_map[current_node_tuple[1][-1]][node]
				dist_cost = dis_map[node][end]
				cost_till_now = time_taken_for_each_node[current_node_tuple[1][-1]]
				
				new_cost = time_cost+cost_till_now
				priority_in_queue = new_cost + dist_cost

				# #Check if node is present in the time taken dictionary if it isn't add
				# #if it is then update time
				if node not in time_taken_for_each_node.keys() or time_taken_for_each_node[node]> new_cost:
					time_taken_for_each_node[node]=new_cost
				# 	print("node {}".format(node))
				# 	print("time {} dist {} newcost {}".format(time_cost,dist_cost, new_cost))
				
				# 	#add to heap
					temp = current_node_tuple[1].copy()
					temp.append(node)

					priority_queue.add_node(temp, priority_in_queue)

	return path #"Path can't be found Willie"

#This is a helper class to implement heap queues
class PriorityQueue:

	#init with a list of elements
	def __init__(self):
		self.nodes = []
	#function to check if the queue is empty or not
	def empty(self):
		return len(self.nodes) == 0

	#pushes a node to the heap
	def add_node(self, node_path, priority_in_queue):
		heapq.heappush(self.nodes, (priority_in_queue, node_path))

	#returns a tuple of node name
	def pop_node(self):
		
		# print("popping")
		return heapq.heappop(self.nodes)
