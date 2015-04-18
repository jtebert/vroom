# For evaluating the success of the project:
# - Accuracy of classification
# - Dirt collection rate (over different numbers of time steps/movements)

import matplotlib.pyplot as plt
from dirt_collection import *
from search import *
import numpy as np


def classification_accuracy(map, environment):
    """
    Compare the accuracy of classification in the map to the environment ground-truth
    :param map: Robot's map after exploration and classification
    :param environment: Ground truth map of obstacle classification
    :return: TODO
    """
    # TODO
    # Get number of each type of obstacle
    actual_obstacles = [1, 3, 5, 6, 7, 2]
    classified_obstacles = [1, 2, 5, 4, 8, 3]
    labels = ["Closet", "Corner", "Doorway", "Garbage can", "Litterbox", "Table"]
    return actual_obstacles, classified_obstacles, labels

def all_dirt_collection_rates(state, environment):
    """
    Get the dirt collection rates for various numbers of time steps
    for 3 possible search types (see dirt_collection_rate)
    :param state: RobotState after exploration/classification
    :param environment: EnvironmentMap
    :return: ([num_time_steps], ([actual], [reactive], [ideal])
    """
    max_num_time_steps = 100
    range_num_time_steps = range(max_num_time_steps)
    print "Dirt", len(environment.get_dirt())
    actual_actions, worst_actions, ideal_actions = get_collection_actions(state, environment)

    print "Dirt", len(environment.get_dirt())
    print "Robot env Dirt", len(state.r.environment.get_dirt())

    actual_rates = dirt_collection_rate(state, environment, actual_actions, max_num_time_steps)
    worst_rates = dirt_collection_rate(state, environment, worst_actions, max_num_time_steps)
    ideal_rates = dirt_collection_rate(state, environment, ideal_actions, max_num_time_steps)
    return range(max_num_time_steps), (actual_rates, worst_rates, ideal_rates)


def dirt_collection_rate(state, environment, actions, num_time_steps):
    """
    Move and collect dirt according to the given list of actions
    :param state: RobotState
    :param environment: State of environment
    :return: List of amount of total dirt collected after each time step
    """
    initial_dirt = len(environment.get_dirt())
    dirt_collected = []
    for t in range(len(actions)):
        state = state.generateSuccessor(actions[t])
        remaining = len(state.r.environment.get_dirt())
        dirt_collected.append(initial_dirt - remaining)
    dirt_collected = max_rate_num_time_steps(dirt_collected, num_time_steps)
    return dirt_collected


def max_rate_num_time_steps(rates, num_time_steps):
    """
    Get even-sized arrays of rates and fill extras
    :param rates: Array of amount of dirt collected
    :param num_time_steps: maximum # of time steps
    :return: array of dirt collected with length num_time_steps
    """
    num_actions = len(rates)
    if num_actions > num_time_steps:
        return rates[0:num_time_steps]
    if num_actions == 0:
        return np.zeros(num_time_steps)
    extra = [rates[num_actions - 1]] * (num_time_steps - num_actions)
    rates.extend(extra)
    return rates


def get_collection_actions(state, environment):
    """
    Get the list of dirt collecting actions for:
     - A* search from dirt predictions
     - Naive robot (reactive agent) [lower limit]
     - Ideal search (A* using actual generated dirt) [upper limit]
     """
    actual_state = state.copy()
    problem = CollectDirtProblem(actual_state)
    actual_actions = a_star_search(problem, dirt_heuristic)
    
    # TODO: Use reactive agent
    worst_actions = []

    ideal_state = state.copy()
    ideal_state.map = environment.copyEnvIntoMap(state.map)
    problem = CollectDirtProblem(ideal_state)
    ideal_actions = a_star_search(problem, dirt_heuristic)

    return actual_actions, worst_actions, ideal_actions


def plot_dirt_collection_rates(time_steps, collection_rates):
    """
    Plot the results of all_dirt_collection_rates
    :param time_steps: List of time steps
    :param rates: ([actual], [reactive], [ideal])
    :return: None
    """
    actual_rates, reactive_rates, ideal_rates = collection_rates
    plt.figure()
    plt.title('Dirt Collection Rates')
    plt.xlabel('Time Steps')
    plt.ylabel('Total Dirt Collected')
    actual_h, = plt.plot(time_steps, actual_rates, linewidth=3, color='b')
    reactive_h, = plt.plot(time_steps, reactive_rates, linewidth=2, color='r')
    ideal_h, = plt.plot(time_steps, ideal_rates, linewidth=2, color='g')
    plt.legend([actual_h, reactive_h, ideal_h], ['Actual Rate', 'Reactive Agent Rate', 'Ideal Rate'])
    plt.show()


def plot_classification_accuracy(actual, classified, labels):
    """
    Plot the classification accuracy of # of each type of obstacle found
    Each is a list:
    [closet, corner, doorway, garbage can, litterbox, table]
    :param actual: ground truth from environment
    :param classified: output of classifier
    :param labels: Names of the obstacle types (in order)
    :return: None
    """
    print actual
    print classified
    fig, ax = plt.subplots()
    ind = np.arange(len(actual))
    width = 0.35
    rects1 = ax.bar(ind, actual, width, color='g', edgecolor=None)
    rects2 = ax.bar(ind + width, classified, width, color='r', edgecolor=None)

    ax.set_xlabel('Obstacle Category', fontweight='bold')
    ax.set_ylabel('Number Found', fontweight='bold')
    ax.set_title('Classification Accuracy')
    ax.legend([rects1, rects2], ['Actual', 'Classified'], loc='best', frameon=False)
    ax.set_xticks(ind + width)
    ax.set_xticklabels(labels)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    plt.show()
