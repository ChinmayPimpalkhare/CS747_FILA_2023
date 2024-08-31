import os
import sys
import random 
import json
import math
import utils
import time
import config
import numpy
random.seed(73)

#Through our experiments, we can conclude that the standard deviation 
# of the noise is varying linearly with force as f*3/100 
 

def get_distance(arr1, arr2):
    return numpy.linalg.norm(arr1 - arr2)

#The first vector represents the tail, the second vector represents the head
def get_unit_vector(arr1, arr2): 
    vec = arr2 - arr1
    dist = numpy.linalg.norm(arr2 - arr1)
    if dist == 0:
        dist = 10e-8
    return numpy.array((vec[0]/dist, vec[1]/dist))

def compute_angle(vec1, vec2): 
    cos_angle = numpy.dot(vec1, vec2)/(numpy.linalg.norm(vec1) * numpy.linalg.norm(vec2))
    angle = numpy.arccos(cos_angle)
    if angle <= numpy.pi/2: #We are in the lower half plane! 
        if (vec1[0]*vec2[1] - vec2[0]*vec1[1] >= 0):  
            return angle/numpy.pi
        elif (vec1[0]*vec2[1] - vec2[0]*vec1[1] < 0): 
            return -angle/numpy.pi
        
def compute_angle_on_screen(vec):
    reference_vector = numpy.array((0,1))
    cos_angle = numpy.dot(reference_vector, vec)/ \
        (numpy.linalg.norm(reference_vector) * numpy.linalg.norm(vec))
    if cos_angle >= 0: #Lies in the lower halfplane
        if ((reference_vector[0]*vec[1] - reference_vector[1]*vec[0]) < 0): 
            angle = numpy.arccos(cos_angle)/numpy.pi - 1 
            return angle
        elif ((reference_vector[0]*vec[1] - reference_vector[1]*vec[0]) >= 0):
            angle = 1 - numpy.arccos(cos_angle)/numpy.pi 
            return angle 
    elif cos_angle < 0: #Lies in the upper halfplane 
        if ((reference_vector[0]*vec[1] - reference_vector[1]*vec[0]) < 0): 
            angle = numpy.arccos(cos_angle)/numpy.pi - 1 
            return angle
        elif ((reference_vector[0]*vec[1] - reference_vector[1]*vec[0]) >= 0):
            angle = 1 - numpy.arccos(cos_angle)/numpy.pi 
            return angle 


def compute_best_hole_angle(ball_pos, hole_list):
    best_dict = {}
    white_location = numpy.array((ball_pos["white"][0], ball_pos["white"][1]))
    for i in range(1, 10): 
        if ball_pos.get(i) != None: 
            ball_location = numpy.array((ball_pos[i][0], ball_pos[i][1]))
            unit_vector_white_to_ball = get_unit_vector(white_location, ball_location)
            list_per_ball = numpy.zeros(6)
            for j in range(0, 6):
                hole_location = numpy.array((hole_list[j]))
                #print(hole_location, ball_location, white_location)
                vector_to_hole = get_unit_vector(ball_location, hole_location)
                dot_product = numpy.dot(unit_vector_white_to_ball, vector_to_hole)
                list_per_ball[j] = dot_product
            #print(list_per_ball)
            best_hole = numpy.max(list_per_ball)
            best_dict[i] = best_hole
    return best_dict
             
    
def check_which_ball_is_closest_to_white(ball_pos): 
    distances = {}
    white_location = numpy.array(ball_pos["white"])
    for i in range(1, 10):
        if ball_pos.get(i) != None: 
            color_location = numpy.array(ball_pos[i])
            distance = get_distance(white_location, color_location)
            distances[i] = distance
    closest_ball = min(zip(distances.values(), distances.keys()))[1]
    closest_distance = distances[closest_ball]
    return distances, closest_distance, closest_ball
    
def check_which_ball_is_closest_to_a_hole(ball_pos, hole_list): 
    hole_distances = {}
    for i in range(0, 10): 
        if ball_pos.get(i) != None: 
            color_location = numpy.array(ball_pos[i])
            distance_from_each_hole = numpy.zeros(6)
            for j in range(0,6):
                hole_array = numpy.array(hole_list[j])
                dist = get_distance(color_location, hole_array)
                distance_from_each_hole[j] = dist
            hole_distances[i] = numpy.min(distance_from_each_hole)
    print(hole_distances)
    closest_to_hole = min(zip(hole_distances.values(), hole_distances.keys()))[1]
    closest_to_hole_distance = hole_distances[closest_to_hole]
    return hole_distances, closest_to_hole_distance, closest_to_hole


def best_suited_hole_and_dangle(ball_pos, ball, hole_list):
    white_location = numpy.array(ball_pos["white"])
    color_location = numpy.array(ball_pos[ball])
    unit_vector_from_white_to_color = get_unit_vector(white_location, color_location)
    an_array_of_hole_goodness = numpy.zeros(6)
    for i in range(0,6): 
        hole_array = numpy.array(hole_list[i])
        unit_vector_color_to_hole = get_unit_vector(color_location, hole_array)
        dot_product_which_tells_goodness = numpy.dot(unit_vector_color_to_hole, \
                                                     unit_vector_from_white_to_color)
        an_array_of_hole_goodness[i] = dot_product_which_tells_goodness
    best_hole_to_aim = numpy.argmax(an_array_of_hole_goodness)
    goodness_value_of_the_best_hole = numpy.max(an_array_of_hole_goodness)
    return an_array_of_hole_goodness, goodness_value_of_the_best_hole, best_hole_to_aim


def dict_of_angles(ball_pos, ball, hole_list):
    white_location = numpy.array(ball_pos["white"])
    color_location = numpy.array(ball_pos[ball])
    unit_vector_from_white_to_color = get_unit_vector(white_location, color_location)
    angdict = {}
    for i in range(0,6): 
        hole_array = numpy.array(hole_list[i])
        unit_vector_color_to_hole = get_unit_vector(color_location, hole_array)
        dot_product_which_tells_goodness = numpy.dot(unit_vector_color_to_hole, \
                                                     unit_vector_from_white_to_color)
        angdict[i] = dot_product_which_tells_goodness
    return angdict

def set_mu_and_force(goodness, distance=1000): 
    goodness_threshold = 0.1 #Goodness_Threshold
    distance_threshold = 80#Distance_Threshold
    maximum_force = 0.75
    min_force = 0.62
    force_if_too_close = 0.6
    force_of_direct_hit = 0.8
    if goodness > goodness_threshold: 
        mu = 2
        if distance <= distance_threshold: 
            force = force_if_too_close
        else: 
            force = numpy.minimum(maximum_force - (maximum_force - min_force)*goodness**1, 1) 
    else: 
        print("Entering else loop")
        mu = 0
        force = force_of_direct_hit
    return mu, force


#Returns the normalized angle which needs to be passed to the action function if
# a position is reachable, otherwise it returns None
def hit_ball_to_hole(ball_pos, hole_list, ball, hole, mu_value=2): 
    hole_location = numpy.array(hole_list[hole])  
    mu = mu_value
    #print("Hole location :", hole_location)
    ball_location = numpy.array((ball_pos[ball][0], ball_pos[ball][1]))
    #print("Ball location: ", ball_location)
    direction_from_ball_to_hole = get_unit_vector(ball_location, hole_location)
    #print("Unit vector from ball to hole: ", direction_from_ball_to_hole)
    ball_radius = config.ball_radius
    ideal_center_x = ball_location[0] - mu*direction_from_ball_to_hole[0]*ball_radius
    ideal_center_y = ball_location[1] - mu*direction_from_ball_to_hole[1]*ball_radius
    ideal_center  = numpy.array((ideal_center_x, ideal_center_y))
    #print("Ideally we want white to hit at: ", ideal_center)
    white_location = numpy.array((ball_pos["white"][0], ball_pos["white"][1]))
    #print("Currently white is at: ", white_location)
    distance_ball_and_white = get_distance(ball_location, white_location)
    #print("Distance between centers of ball and white:" , distance_ball_and_white)
    distance_ideal_and_white = get_distance(ideal_center, white_location)
    #print("Distance between the ideal center and white:", distance_ideal_and_white)
    threshold_distance = numpy.sqrt(numpy.maximum(distance_ball_and_white**2 - \
                                               mu*mu*(ball_radius**2), 0))*1.05
    #print("The threshold distance is:", threshold_distance)8
    if distance_ideal_and_white <= threshold_distance:
        #print("Point is reachable")
        vector_white_to_ideal = get_unit_vector(white_location, ideal_center)
        #print("Unit vector in the direction is:", vector_white_to_ideal)
        angle = compute_angle_on_screen(vector_white_to_ideal)
        #print("Angle to be moved in:", angle)
        return angle
    #else:
        #print("Cannot reach given point, returning None!")


class Agent:
    def __init__(self, table_config) -> None:
        self.table_config = table_config
        self.prev_action = None
        self.curr_iter = 0
        self.state_dict = {}
        self.holes =[]
        self.ns = utils.NextState()


    def set_holes(self, holes_x, holes_y, radius):
        for x in holes_x:
            for y in holes_y:
                self.holes.append((x[0], y[0]))
        self.ball_radius = radius


    def action(self, ball_pos=None):
        ## Code you agent here ##
        ## You can access data from config.py for geometry of the table, configuration of the levels, etc.
        ## You are NOT allowed to change the variables of config.py (we will fetch variables from a different file during evaluation)
        ## Do not use any library other than those that are already imported.
        ## Try out different ideas and have fun! 
          print("Number of balls remaining", len(ball_pos) - 2)
          closeness, _, _ = check_which_ball_is_closest_to_white(ball_pos)
          sorted_closeness = dict(sorted(closeness.items(), key = lambda x:x[1]))
          #print("Closeness:", closeness)
          #print("Sorted closeness:", sorted_closeness)
          count = 0
          for key in sorted_closeness: 
              #print("Key:", key)
              angdict = dict_of_angles(ball_pos, key, self.holes)
              #print("Dictionary of dot products: ", angdict)
              sorted_angdict = dict(sorted(angdict.items(), key = lambda x:x[1], reverse=True)[0:3])
              #print("Sorted angle dictionary:", sorted_angdict)
              for yek in sorted_angdict:                         
                  if hit_ball_to_hole(ball_pos, self.holes, key, yek) != None:
                    angle = hit_ball_to_hole(ball_pos, self.holes, key, yek)
                    miter = 12
                    for k in range(0,miter): 
                        force = 0.3 + (0.6 - 0.3)/miter*k
                        #print("Count is:", count)
                        count += 1 
                        if len(self.ns.get_next_state(ball_pos, (angle, force), numpy.random.randint(0,1000))) < \
                            len(ball_pos):    
                                print("Ball:", key, "Hole:", yek, "Angle:", angle, "Force:", force) 
                                return (angle, force)
          if len(ball_pos) > 3: 
            print("Random shot")
            random_key = random.choice(list(sorted_closeness))
            angle = hit_ball_to_hole(ball_pos, self.holes, random_key, numpy.random.randint(0,5), 0)
            return (angle , 0.5)
          else:
              print("Controlled random shot")
              random_key = random.choice(list(sorted_closeness))
              angle = hit_ball_to_hole(ball_pos, self.holes, random_key, numpy.random.randint(0,5), 0)
              return (angle , 0.5)
              