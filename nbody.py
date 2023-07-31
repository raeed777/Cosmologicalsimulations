import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# constants
G = 2.0  # for simplicity take Newtons constant to be one
m = 1.0  # each mass is 1
epsilon = 0.1  # leap frog
size = 10  # the initial size of the space the particles live in (size * size * size)
num_particles = 1000  # the number of particles
dimensions = 3  # number of dimensions
center = 0

# arrays to hold the particles positions and velocities
positions = []
velocities = []


# set the initial positions and velocities:
for i in range(num_particles):
    # initial velocities is zero
    velocities.append([0, 0, 0])

    # initial position is random between -5 to 5 in each direction, the distribution is uniform
    x = np.random.uniform(-size / 2, size / 2, size=None)
    y = np.random.uniform(-size / 2, size / 2, size=None)
    z = np.random.uniform(-size / 2, size / 2, size=None)
    r = np.sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2))
    positions.append([x, y, z, r])


# function that calculates the force between two masses, take the force acting on the first
def force(position_1, position_2):
    distance = 0
    for dim in range(dimensions):
        distance = distance + pow(position_2[dim]-position_1[dim], 2)
    distance = np.sqrt(distance + pow(epsilon, 2))

    force_vec = []
    for dim in range(dimensions):
        force_vec.append(G * m * m * (position_2[dim]-position_1[dim]) / pow(distance, 3))

    return force_vec


# function that adds two vectors
def add_vec(vec_1, vec_2):
    new_vec = []
    for i in range(dimensions):
        new_vec.append(vec_1[i] + vec_2[i])
    return new_vec


# function that takes a position of a particle and calculates the radius
def calc_r(position):
    r_squared = 0
    for i in range(dimensions):
        r_squared = r_squared + pow(position[i], 2)
    r = np.sqrt(r_squared)
    return r


# function that moves the particles to the next positions
def move_particles(position_list, velocity_list, time_interval):
    for num in range(num_particles):
        new_r = 0
        dist_to_travel = [item * h for item in velocity_list[num]]
        position_list[num] = add_vec(position_list[num], dist_to_travel)
        position_list[num].append(calc_r(position_list[num]))
    return position_list


# function that sorts the positions list by radius, from longest to shortest
def sort_positions(position_list):
    position_list.sort(key=lambda x:x[dimensions], reverse=True)


# function that calculates the density inside a given radius
def density_in_r(r, position_list):
    total_mass_in_r = 0
    for num in range(num_particles):
        if position_list[num][dimensions] < r:
            total_mass_in_r = total_mass_in_r + m
    density = total_mass_in_r / (4 * np.pi * pow(r, 3) / 3)
    return density


# simulation parameters:
h = 0.01  # time intervals
steps = 100  # number of steps
time_values = np.zeros(steps)  # array to hold time steps
radius = 1  # the radius we want to monitor
density_values = np.zeros(steps)  # array to hold the density inside the monitored radius
particles = []  # array to hold (x,y) coordinates through time to present a dynamic scatter

# initializing
sort_positions(positions)
density_values[0] = density_in_r(radius, positions)
for num in range(num_particles):
    x = positions[num][0]
    y = positions[num][1]
    coord = [x, y]
    particles.append(coord)


# simulation
for step in range(1, steps):
    t = time_values[step - 1]
    force_values = []
    for particle in range(num_particles):
        total_force = [0, 0, 0]
        for other_particle in range(particle + 1, num_particles):
            total_force = add_vec(total_force, force(positions[particle], positions[other_particle]))
        vel_diff = [item * h for item in total_force]
        velocities[particle] = add_vec(velocities[particle], vel_diff)
    # now move the particles
    positions = move_particles(positions, velocities, h)
    for num in range(num_particles):
        x = positions[num][0]
        y = positions[num][1]
        coord = [x, y]
        particles.append(coord)
    # calculate the new density inside radius
    density_values[step] = density_in_r(radius, positions)
    time_values[step] = t + h

plt.plot(time_values, density_values, label='density inside r=3')
plt.xlabel('Time')
plt.legend()
plt.show()


f = plt.figure()
for i in range(steps):
    x = []
    y = []
    for num in range(num_particles):
        x.append(particles[num + i * num_particles][0])
        y.append(particles[num + i * num_particles][1])

    # Mention x and y limits to define their range
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)

    # Plotting graph
    plt.scatter(x, y, color='green')
    plt.pause(0.01)
    f.clear()

plt.show()

