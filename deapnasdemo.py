import multiprocessing
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

from tensornas.core.individual import Individual

# Training MNIST data
(
    (images_train, labels_train),
    (images_test, labels_test),
) = tf.keras.datasets.mnist.load_data()
input_shape = images_train.shape
images_train = images_train.reshape(
    images_train.shape[0], images_train.shape[1], images_train.shape[2], 1
)
images_test = images_test.reshape(
    images_test.shape[0], images_test.shape[1], images_test.shape[2], 1
)
mnist_input_tensor_shape = (images_test.shape[1], images_test.shape[2], 1)
images_train = images_train.astype("float32")
images_test = images_test.astype("float32")
images_train /= 255
images_test /= 255
mnist_class_count = 10

# Tensorflow parameters
epochs = 1
batch_size = 600
pop_size = 10

# Functions used for EA demo

# Create a NAS model individual from one of the two demo models
# Creating an iterable that is fed into initIterate


def get_block_architecture():
    from tensornas.blocktemplates.blockarchitectures.classificationblockarchitectures import (
        ClassificationBlockArchitecture,
    )

    """
    This function is responsible for creating and returning the block architecture that an individual shuld embed
    """
    return ClassificationBlockArchitecture(mnist_input_tensor_shape, mnist_class_count)


# Evaluation function for evaluating an individual. This simply calls the evaluate method of the TensorNASModel class
def evaluate_individual(individual):
    return individual.evaluate(
        images_train, labels_train, images_test, labels_test, epochs, batch_size
    )


# Note: please take note of arguments and return forms!
def crossover_individuals(ind1, ind2):
    # TODO
    return ind1, ind2


def mutate_individual(individual):
    return (individual.mutate(),)


def pareto_dominance(ind1, ind2):
    return tools.emo.isDominated(ind1.fitness.values, ind2.fitness.values)


# We want to minimize param count and maximize accuracy
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))

# Each individual will be an architecture model
creator.create("Individual", Individual, fitness=creator.FitnessMulti)

toolbox = base.Toolbox()

### Multithreading ###
pool = multiprocessing.Pool()
toolbox.register("map", pool.map)
######

toolbox.register("get_block_architecture", get_block_architecture)

toolbox.register(
    "individual",
    tools.initRepeat,
    creator.Individual,
    toolbox.get_block_architecture,
    n=1,
)

toolbox.register("population", tools.initRepeat, list, toolbox.individual, n=pop_size)

# Genetic operators
toolbox.register("evaluate", evaluate_individual)
toolbox.register("mate", crossover_individuals)
toolbox.register("mutate", mutate_individual)
toolbox.register("select", tools.selTournament, tournsize=3)

# Statistics
history = tools.History()

toolbox.decorate("mate", history.decorator)
toolbox.decorate("mutate", history.decorator)


# toolbox.decorate("evaluate", history.decorator)


def main():

    test_ind = toolbox.individual()
    ba = next(test_ind.block_architecture)

    pop = toolbox.population(n=3)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)

    pop, logbook = algorithms.eaSimple(
        pop,
        toolbox,
        cxpb=0.5,
        mutpb=0.2,
        ngen=2,
        stats=stats,
        halloffame=hof,
        verbose=True,
    )

    return pop, logbook, hof


if __name__ == "__main__":
    pop, log, hof = main()
    best_individual = hof[0]
    print(
        "Best individual is: %s\nwith fitness: %s"
        % (best_individual, best_individual.fitness)
    )
    best_individual.print()

    gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)
    plt.plot(gen, avg, label="average")
    plt.plot(gen, min_, label="minimum")
    plt.plot(gen, max_, label="maximum")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(loc="lower right")

    # Pareto
    dominated = [
        ind
        for ind in history.genealogy_history.values()
        if pareto_dominance(best_individual, ind)
    ]
    dominators = [
        ind
        for ind in history.genealogy_history.values()
        if pareto_dominance(ind, best_individual)
    ]
    others = [
        ind
        for ind in history.genealogy_history.values()
        if not ind in dominated and not ind in dominators
    ]

    plt.subplot(1, 3, 2)
    for ind in dominators:
        plt.plot(ind.fitness.values[0], ind.fitness.values[1], "r.", alpha=0.7)
    for ind in dominated:
        plt.plot(ind.fitness.values[0], ind.fitness.values[1], "g.", alpha=0.7)
    for ind in others:
        plt.plot(ind.fitness.values[0], ind.fitness.values[1], "k.", alpha=0.7, ms=3)
    plt.plot(
        best_individual.fitness.values[0], best_individual.fitness.values[1], "bo", ms=6
    )
    plt.xlabel("$f_1(\mathbf{x})$")
    plt.ylabel("$f_2(\mathbf{x})$")
    plt.xlim((0.5, 3.6))
    plt.ylim((0.5, 3.6))
    plt.title("Objective space")
    plt.tight_layout()

    non_dom = tools.sortNondominated(
        history.genealogy_history.values(),
        k=len(history.genealogy_history.values()),
        first_front_only=True,
    )[0]

    plt.subplot(1, 3, 3)
    for ind in history.genealogy_history.values():
        plt.plot(ind.fitness.values[0], ind.fitness.values[1], "k.", ms=3, alpha=0.5)
    for ind in non_dom:
        plt.plot(ind.fitness.values[0], ind.fitness.values[1], "bo", alpha=0.74, ms=5)
    plt.title("Pareto-optimal front")

    plt.show()
