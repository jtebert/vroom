# For evaluating the success of the project:
# - Accuracy of classification
# - Dirt collection rate (over different numbers of time steps/movements)

import matplotlib.pyplot as plt
from dirt_collection import *
from search import *


def classification_accuracy(map, environment):
    """
    Compare the accuracy of classification in the map to the environment ground-truth
    :param map: Robot's map after exploration and classification
    :param environment: Ground truth map of obstacle classification
    :return: TODO
    """
    # TODO

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
    actual_rates = []
    worst_rates = []
    ideal_rates = []
    for num_time_steps in range_num_time_steps:
        actual, worst, ideal  = dirt_collection_rate(state, environment, num_time_steps)
        actual_rates.append(actual)
        worst_rates.append(worst)
        ideal_rates.append(ideal)
    return (range_num_time_steps, (actual_rates, worst_rates, ideal_rates))


def dirt_collection_rate(state, environment, num_time_steps):
    """
    Compare dirt collection rates for:
    - A* search from dirt predictions
    - Naive robot (reactive agent) [lower limit]
    - Ideal search (A* using actual generated dirt) [upper limit]
    :param state: RobotState after exploration/classification
    :param environment: EnvironmentMap
    :return: tuple (actual, reactive, ideal) of amount of dirt collected
    """
    initial_dirt = len(state.environment.map.getDirt())
    # TODO
    # Do actual search
    actual_state = state.copy()
    problem = CollectDirtProblem(actual_state)
    actions = a_star_search(problem, dirt_heuristic)
    execute_actions = actions[0:num_time_steps]
    actual_state.executeActions(execute_actions)
    remaining_dirt = len(actual_state.environment.map.getDirt())
    actual_collected = initial_dirt - remaining_dirt

    # Do worst search
    # Reactive agent? (not sure where this is)
    worst_collected = initial_dirt - remaining_dirt

    # Copy environment into map and do ideal search
    ideal_state = state.copy()
    ideal_state.map = environment.copyEnvIntoMap(state.map)
    problem = CollectDirtProblem(ideal_state)
    actions = a_star_search(problem, dirt_heuristic)
    execute_actions = actions[0:num_time_steps]
    actual_state.executeActions(execute_actions)
    remaining_dirt = len(ideal_state.environment.map.getDirt())
    ideal_collected = initial_dirt - remaining_dirt

    return (actual_collected, worst_collected, ideal_collected)


def plot_dirt_collection_rates(rates):
    """
    Plot the results of all_dirt_collection_rates
    :param rates: ([num_time_steps], ([actual], [reactive], [ideal])
    :return: None
    """
    num_time_steps, collection_rates = rates
    actual_rates, reactive_rates, ideal_rates = collection_rates
    plt.figure()
    actual_h, = plt.plot(num_time_steps, actual_rates, linewidth=3, color='b')
    reactive_h, = plt.plot(num_time_steps, reactive_rates, linewidth=2, color='r')
    ideal_h, = plt.plot(num_time_steps, ideal_rates, linewidth=2, color='g')
    plt.legend([actual_h, reactive_h, ideal_h], ['Actual Rate', 'Reactive Agent Rate', 'Ideal Rate'])