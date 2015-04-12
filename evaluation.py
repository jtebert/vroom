# For evaluating the success of the project:
# - Accuracy of classification
# - Dirt collection rate (over different numbers of time steps/movements)

import matplotlib.pyplot as plt


def classification_accuracy(map, environment):
    """
    Compare the accuracy of classification in the map to the environment ground-truth
    :param map: Robot's map after exploration and classification
    :param environment: Ground truth map of obstacle classification
    :return: TODO
    """

def all_dirt_collection_rates(state, environment):
    """
    Get the dirt collection rates for various numbers of time steps
    for 3 possible search types (see dirt_collection_rate)
    :param state: RobotState after exploration/classification
    :param environment: EnvironmentMap
    :return: ([num_time_steps], ([actual], [reactive], [ideal])
    """
    return ([], ([], [], []))


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
    # Do actual search
    # Do worst search
    # Copy environment into map and do ideal search


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