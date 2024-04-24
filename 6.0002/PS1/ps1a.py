###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: Ray O
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # Create dictionary.
    cow_dict = {}
    # Open and file.
    with open(filename, encoding = "utf-8") as f:
        # Loop over the file by line.
        for line in f:
            # Remove the newline \n.
            line = line[:-1]
            # Split the lines into name and weight.
            tmp = line.split(",")
            # Add to the dictionary (make the weight an int).
            cow_dict[tmp[0]] = int(tmp[1])
    return cow_dict


# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # Initialize variables.
    cargo_weight = 0
    cargo = []
    res = []
    # Create a copy of cows dict.
    copy_cows_dict = cows.copy()
    # Loop until all cows are in the results.
    while copy_cows_dict != {}:
        # Create a sorted list from cows dictionary.
        copy_cows = sorted(copy_cows_dict.items(), key=lambda x:x[1], reverse=True)
        # Loop over sorted list.
        for i in range(len(copy_cows)):
            # If the weight doesn't exceed 10,
            if cargo_weight+(copy_cows[i])[1] <= limit:
                # Add cow at index i to the cargo
                cargo.append((copy_cows[i])[0])
                cargo_weight += (copy_cows[i])[1]
            else:
                break
        # Add result of for loop to results.
        res.append(cargo)
        # Delete cows that were already used once. 
        for c in cargo:
            if c in copy_cows_dict:
                del copy_cows_dict[c]
        # Reset cargo and weight.
        cargo = []
        cargo_weight = 0
    return res


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # Initiate the best set(the highest number of trips).
    bestSet = cows
    # Initiate flag to check if cargo weight is exceeded.
    flag = True
    # For loop over each partition.
    for partition in get_partitions(cows):
        # For loop over each trip.
        for cargo in partition:
            # Reset cargo weight to zero.
            cargo_weight = 0
            # For loop over each cow.
            for cow in cargo:
                # Append to cargo weight the cows weight.
                cargo_weight+=cows.get(cow)
                # If cargo weight exceeds the limit, set flag to false.
                if cargo_weight > limit:
                    flag = False
                    break
        # If flag is true, and the trip number is better than the best so far
        # set the best to the new best.
        if flag and len(partition) < len(bestSet):
            bestSet = partition
        # Reset flag.
        flag = True
    return(bestSet)


# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    data = 'ps1_cow_data_2.txt'

    start = time.time()
    ## code to be timed
    x = greedy_cow_transport(load_cows(data),limit=10)
    print(x)
    end = time.time()
    print ('greedy: ',end - start)


    start = time.time()
    ## code to be timed
    m = brute_force_cow_transport(load_cows(data))
    print(m)
    end = time.time()
    print ('brute: ', end - start)
    
compare_cow_transport_algorithms()




