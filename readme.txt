====================================================================================================
           '   +++      ++;:++++++++;   '+++++++   :+++++++:  ++       ++' ++
 ;+++++++++++  +++     +++ ++++++++++  ++++++++++ ++++++++++  +++     +++  ++       ++++++++++++'
           ;'   ++    :++         +++  ++     +++ ++;     ++ :+++    '+++ ;++    ++++++++++++++++++
                ++;   ++          +++ '++     +++ ++      ++ +++++   ++++ +++   ++++++++++++++++++++
     ;'+++++++  +++  +++   +++++++++' +++     ++  ++     '++ +++++  +++++ ++:  +++++++++++++++++++++
        ,;'+++   ++ +++    +++++++++  ++:     ++ ;++     +++ ++ ++;++++++ ++   +++++++++++++++     '
                 ++;++    +++  +++    ++      ++ +++     ++  ++ +++++ ++       ++++++++++++++++
         ;'++++  ++++'    +++   +++   ++++++++++ ++++++++++ :++ ;+++  ++ ;++   +++++++++++++++++
      :'+++++++   +++     ++    ;+++  +++++++++  ++++++++++ +++  ++   ++ +++     +++       +++
====================================================================================================


The VROOM simulator features command line options to run various components of the project.

This project works with python 2.7 and requires the following dependencies:
   -> pygame
   -> matplotlib
   -> numpy

The latest version of each dependency that supports python 2.7 should work fine.

Most of the simulator can run with pygame alone, though the evaluation graphs will need matplotlib\numpy.

Here is a recommended walk through of the simulator.

Set the current directory to robotoverloards\simulator.

> python simulator.py 

This will let you explore the default environment ("../assets/maps/test.csv"). 
The default screen is the robots map of the world. To view the environment press e. When
viewing the environment, you can press "l" to view the ground truth labels.
As the robot cleans it will add dirt readings to the map (blue) and remove the
dirt from the environment.

> python simulator.py -x

This will demo the robot exploring an environment using depth first search + back tracking. 
Normally this step is done in the background, but this option provides a visualization of the search
algorithm.

> python simulator.py -s

This will perform the exploration phase, update the environment with dirt,
update the robots map with dirt, then perform an a_start_search.

Note there can be a pause of significant lenght (~30 seconds or so) for 
searching the environment as there can be a lot of possible states for the robot to 
explore to pick up all the dirt. Once the pygame window loads it will 
demonstrate the path a_star returned to pick up where it thinks the dirt is.
This mode copies the obstacle labels from the environment which results in
perfect classification.

> python simulator.py -f

This will perform feature extraction -> classification of a direct copy of the environment.
Unfortunately this feature is not complete and is misclassifying obstacles.

> python simulator.py -s -v

This will perform an exploration of the environment, and then perform an evaluation on the robot.
In this case classification accuracy will have perfect results as the obstacle labels are directly 
copied into the robots map.  Close the classification accuracy graph to continue the simulation.
Note this next phase will take ~1-2 minutes to run the two search algorithms.

The dirt collection rates graph displays the ideal, actual, and worst dirt pickup rates.
The ideal rate is the rate of dirt pickup if the a_star search was executed on a copy 
of the environment. The actual rate is the dirt pickup rate using the robots predictions of the
dirt location. The worst dirt pickup rate is using a basic reactive agent that explores 
most of the environment. In this case since the obstacle labeling is copied into the robots map 
(perfect classification) the actual rate will be comparable to the ideal rate.


> python simulator.py -a 

This will perform exploration -> feature extraction -> classification -> search\classification evaluation.

The same comments apply to the above option though this time the robot will attempt to classify the environment
with its own classifier as opposed to just copying over the true classifications. Since the classification
accuracy is poor, the actual dirt collection rate will not reach the ideal rate as it is not cleaning 
all of the obstacles in the environment.

> python simulator.py (any above option) -e "../assets/maps/"other test map"  

If you provide an input to another one of our test maps you can see the robot explore different environments.

Another good example is "../assets/maps/newHouse.csv". This map has multiple rooms and obstacles for the robot 
to clean. But note, this is a larger map and can take up to 3-5 minutes to perform the search algorithm.
