
"""
Module name: ConjecTuring
Author: Adrián Fidalgo Díaz
Date: April 4, 2023

Provides functions to perform conjecture checking (battery tests) in an easy way. 
"""

from typing import Generator, Callable
from tqdm import tqdm
from math import inf


def find_counterexample(n: int, condition: Callable[[object], bool], generator: Generator[object, None, None], show_progress: bool = False) -> object:
    """
    Performs several checks of a conjecture over some objects and returns the first one, the first 
    found counterexample, not satisfying it.

    Parameters
    ----------
    n: int
        Number of checkings to perform.
    condition: Callable[[object], boolean]
        The conjecture to check.
    generator: Generator[object, None, None]
        A generator that yields objects for which to check the conjecture. 
    progress_bar: boolean, optional 
        A flag used to print a progress bar (default is False)
    
    Returns
    -------
    object
        An object representing the first counterexample found. If no one is found, returns None.
    """

    # Local function: compute batch
    def compute_batch(length):
        for i in range(length):
            current_object = next(generator)

            # Check if the condition holds for the current object
            if (not condition(current_object)):
                return current_object
        
        return None

    # Print heading
    print("  ________________________________")
    print("  Find counterexample", n, "times")
    print("  - Generator:", generator.__name__) 
    print("  - Condition:", condition.__name__)
    print("  ________________________________")
    print("")

    # Prepare batch length
    UPDATE_RATIO = 100
    progress_bar = tqdm(range(n), leave=False)

    batch_length = n // UPDATE_RATIO   
    remaining_length = n % UPDATE_RATIO

    listOfBatches = [ (batch_length + 1) for i in range(remaining_length) ] + [(batch_length) for i in range(UPDATE_RATIO-remaining_length)]

    # Loop of checkings
    for batch in listOfBatches:
        current_result = compute_batch(batch)        

        # Update progress bar
        progress_bar.update(batch)

        # Check if checking is done
        if current_result is not None:
            # Close the progress bar
            progress_bar.close()

            # Print an end message
            print("  Result: found counterexample!")
            print("  -->", str(current_result))

            return current_result

    # Close the progress bar
    progress_bar.close()

    # Print a no concluding message
    print("  Result: no concluding.")

    return None 


def count_counterexamples(n: int, condition: Callable[[object], bool], generator: Generator[object, None, None], show_progress: bool = False) -> int:
    """
    Counts the number of objects given by the generator within n iterations that do not satisfy the given
    condition (counts the number of counterxamples).

    Parameters
    ---------- 
    n: int
        Number of checkings to perform.
    condition: Callable[[object], boolean]
        The conjecture to check.
    generator: Generator[object, None, None]
        A generator that yields objects for which to check the conjecture. 
    progress_bar: boolean, optional 
        A flag used to print a progress bar (default is False)
    
    Returns
    -------
    int
        The number of counterexamples found.
    """

    # Local function: compute batch
    def compute_batch(length):
        local_count = 0

        for i in range(length):
            current_object = next(generator)

            # Check if the condition holds for the current object
            if (not condition(current_object)):
                local_count += 1

        return local_count
        
    # Print heading
    print("  ________________________________")
    print("  Count counterexamples", n, "times")
    print("  - Generator:", generator.__name__) 
    print("  - Condition:", condition.__name__)
    print("  ________________________________")
    print("")

    # Prepare batch length
    UPDATE_RATIO = 100
    progress_bar = tqdm(range(n), leave=False)

    batch_length = n // UPDATE_RATIO   
    remaining_length = n % UPDATE_RATIO

    listOfBatches = [ (batch_length + 1) for i in range(remaining_length) ] + [(batch_length) for i in range(UPDATE_RATIO-remaining_length)]

    # Count counterexamples
    number_of_counterexamples = 0

    # Loop of checkings
    for batch in listOfBatches:
        number_of_counterexamples += compute_batch(batch)

        # Update the progress bar
        progress_bar.update(batch)

    # Print an end message
    print("  Result:", number_of_counterexamples, "counterexamples found!")

    return number_of_counterexamples 


def smallest_counterexample(n: int, condition: Callable[[object], bool], generator: Generator[object, None, None], get_object_weight: Callable[[object], int], show_progress: bool = False) -> object:
    """
    Finds the smallest object, in terms of the getObjectWeight function, that does not satisfies the conjecture
    given by the condition function.

    Parameters
    ---------- 
    n: int
        Number of checkings to perform.
    condition: Callable[[object], boolean]
        The conjecture to check.
    generator: Generator[object, None, None]
        A generator that yields objects for which to check the conjecture. 
    getObjectWeight: Callable[[object], int]
        A function that gives the weight of an object by returning an int.
    progress_bar: boolean, optional 
        A flag used to print a progress bar (default is False)
    
    Returns
    -------
    object
        The counterexample with the smallest weight between the computed ones.
    """

    # Local function: compute batch
    def compute_batch(length):
        local_smallest_counterexample = None
        local_smallest_weight = int("inf")

        for i in range(length):
            current_object = next(generator)

            # Check if the condition holds for the current object
            if (not condition(current_object)):
                current_weight = get_object_weight(current_object)
                if (current_weight < local_smallest_weight):
                    local_smallest_counterexample = current_object
                    local_smallest_weight = current_weight

        return (local_smallest_counterexample, local_smallest_weight)

    # Print heading
    print("  ________________________________")
    print("  Find the smallest", n, "times")
    print("  - Generator:", generator.__name__) 
    print("  - Condition:", condition.__name__)
    print("  - Weight:   ", get_object_weight.__name__)
    print("  ________________________________")
    print("")

    # Prepare batch length
    UPDATE_RATIO = 100
    progress_bar = tqdm(range(n), leave=False)

    batch_length = n // UPDATE_RATIO   
    remaining_length = n % UPDATE_RATIO

    listOfBatches = [ (batch_length + 1) for i in range(remaining_length) ] + [(batch_length) for i in range(UPDATE_RATIO-remaining_length)]

    # Lowest counterexample
    smallest_counterexample = None
    smallest_weight = int("inf")

    # Loop of checkings
    for batch in listOfBatches:
        local_smallest_counterexample, local_smallest_weight = compute_batch(batch)

        if (local_smallest_weight < smallest_weight):
            smallest_counterexample = local_smallest_counterexample
            smallest_weight = local_smallest_weight

        # Update the progress bar
        progress_bar.update(batch)

    # Print a message
    if (smallest_counterexample is None):
        print("  Result:", "no counterexample found.")
    else:
        print("  Result: lowest counterexample")
        print("  -->", str(smallest_counterexample))

    return smallest_counterexample 


def greatest_counterexample(n: int, condition: Callable[[object], bool], generator: Generator[object, None, None], get_object_weight: Callable[[object], int], show_progress: bool = False) -> object:
    """
    Finds the greatest object, in terms of the getObjectWeight function, that does not satisfies the conjecture
    given by the condition function.

    Parameters
    ---------- 
    n: int
        Number of checkings to perform.
    condition: Callable[[object], boolean]
        The conjecture to check.
    generator: Generator[object, None, None]
        A generator that yields objects for which to check the conjecture. 
    getObjectWeight: Callable[[object], int]
        A function that gives the weight of an object by returning an int.
    progress_bar: boolean, optional 
        A flag used to print a progress bar (default is False)
    
    Returns
    -------
    object
        The counterexample with the greatest weight between the computed ones.
    """

    # Local function: compute batch
    def compute_batch(length):
        local_greatest_counterexample = None
        local_greatest_weight = int("-inf")

        for i in range(length):
            current_object = next(generator)

            # Check if the condition holds for the current object
            if (not condition(current_object)):
                current_weight = get_object_weight(current_object)
                if (current_weight > local_greatest_weight):
                    local_greatest_counterexample = current_object
                    local_greatest_weight = current_weight

        return (local_greatest_counterexample, local_greatest_weight)
        
    # Print heading
    print("  ________________________________")
    print("  Find the greatest", n, "times")
    print("  - Generator:", generator.__name__) 
    print("  - Condition:", condition.__name__)
    print("  - Weight:   ", get_object_weight.__name__)
    print("  ________________________________")
    print("")

    # Prepare batch length
    UPDATE_RATIO = 100
    progress_bar = tqdm(range(n), leave=False)

    batch_length = n // UPDATE_RATIO   
    remaining_length = n % UPDATE_RATIO

    listOfBatches = [ (batch_length + 1) for i in range(remaining_length) ] + [(batch_length) for i in range(UPDATE_RATIO-remaining_length)]

    # Greatest counterexample
    greatest_counterexample = None
    greatest_weight = int("-inf")

    # Loop of checkings
    for batch in listOfBatches:
        local_greatest_counterexample, local_greatest_weight = compute_batch(batch)

        if (local_greatest_weight > greatest_weight):
            greatest_counterexample = local_greatest_counterexample
            greatest_weight = local_greatest_weight

        # Update progress bar
        progress_bar.update(batch)

    # Print a message
    if (greatest_counterexample is None):
        print("  Result:", "no counterexample found.")
    else:
        print("  Result: greatest counterexample")
        print("  -->", str(greatest_counterexample))

    return greatest_counterexample 


