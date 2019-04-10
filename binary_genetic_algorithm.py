import random
import sys
import math
import matplotlib.pyplot as plt


# Parameter functions and values


def cost(chromosome):
    x, y = decode_chromosome_function(chromosome)
    return mccormick_function(x, y)


def tournament_selection(cost_f, population, size):
    z = []
    while len(z) < size:
        z.append(random.choice(population))
    best = None
    best_f = None
    for e in z:
        ff = cost_f(e)
        if best is None or ff < best_f:
            best_f = ff
            best = e
    return best


def code_chromosome(x, y):
    x = int(x * math.pow(10, precision))
    y = int(y * math.pow(10, precision))
    x = int(x + 1.5 * math.pow(10, precision))
    y = int(y + 3 * math.pow(10, precision))
    chromosome_x = list(bin(x)[2:].zfill(num_bits_x))
    chromosome_y = list(bin(y)[2:].zfill(num_bits_y))
    return chromosome_x + chromosome_y


def decode_chromosome(chromosome):
    chromosome_x = chromosome[:num_bits_x]
    chromosome_y = chromosome[num_bits_x:]
    x = int(''.join(map(str, chromosome_x)), 2)
    y = int(''.join(map(str, chromosome_y)), 2)
    x -= 1.5 * math.pow(10, precision)
    y -= 3 * math.pow(10, precision)
    x /= math.pow(10, precision)
    y /= math.pow(10, precision)
    return x, y


max_iter = 500
mut_rate = 0.2
population_size = 150
next_population_size = 150
num_runs = 5
convergence_number = 100        # algorithms stops if best chromosome doesn't change for this number of generations
precision = 3
num_bits_x = int(math.ceil(math.log2(5.5 * math.pow(10, precision))))
num_bits_y = int(math.ceil(math.log2(7 * math.pow(10, precision))))
crossover_selection = tournament_selection
cost_function = cost
code_chromosome_function = code_chromosome
decode_chromosome_function = decode_chromosome
outfile = sys.stdout


########################################################################
# Algorithm and fixed functions


def mutate(chromosome, probability):
    if random.random() <= probability:
        first = random.randrange(1, len(chromosome) - 1)
        second = random.randrange(1, len(chromosome) - 1)
        if first < second:
            chromosome[first: second + 1] = reversed(chromosome[first: second + 1])
        else:
            chromosome[second: first + 1] = reversed(chromosome[second: first + 1])
    return chromosome


def mccormick_function(x, y):
    return math.sin(x + y) + (x - y) ** 2 - 1.5 * x + 2.5 * y + 1


def valid_chromosome(chromosome):
    x, y = decode_chromosome_function(chromosome)
    if not (-1.5 <= x <= 4):
        return False
    if not (-3 <= y <= 4):
        return False
    return True


def single_point_crossover(c1, c2):
    r = random.randrange(1, len(c1) - 1)
    c3 = c1[:r] + c2[r:]
    c4 = c2[:r] + c1[r:]
    return c3, c4


def draw_stats(all_best_lists, all_average_lists, generations_list, pop_size):
    c = 0
    colors = ['green', 'blue', 'yellow', 'red', 'orange']
    for best_list in all_best_lists:
        x_number_values = list(range(generations_list[c]))
        y_number_values = best_list
        plt.plot(x_number_values, y_number_values, color=colors[c], label=str(c + 1))
        plt.title('Best solution', fontsize=19)
        plt.xlabel('Generations', fontsize=10)
        plt.ylabel('Function value', fontsize=10)
        plt.tick_params(axis='both', labelsize=9)
        c += 1
    plt.legend(loc='upper right')
    filename = 'best' + str(pop_size) + '.pdf'
    plt.savefig(filename)

    plt.clf()
    c = 0
    for average_list in all_average_lists:
        x_number_values = list(range(generations_list[c]))
        y_number_values = average_list
        plt.plot(x_number_values, y_number_values, color=colors[c], label=str(c + 1))
        plt.title('Average cost function value', fontsize=19)
        plt.xlabel('Generations', fontsize=10)
        plt.ylabel('Function value', fontsize=10)
        plt.tick_params(axis='both', labelsize=9)
        c += 1
    plt.legend(loc='upper right')
    filename = 'average' + str(pop_size) + '.pdf'
    plt.savefig(filename)


def genetski():
    sum_cost = 0
    sum_iterations = 0
    best_ever_sol = None
    best_ever_f = None
    all_best_lists = []
    all_average_lists = []
    generations_list = []
    for k in range(num_runs):
        print('Starting: GA', k + 1, ', population size:', population_size, ', maximum_iterations:', max_iter,
              ', mutation_rate:', mut_rate, ', number of runs:', num_runs, file=outfile)
        best_list = []
        average_list = []
        best = None
        best_f = None
        current_same = 0
        t = 0
        tuple_pop = zip([round(random.uniform(-1.5, 4), precision) for _ in range(population_size)],
                        [round(random.uniform(-3, 4), precision) for _ in range(population_size)])
        population = []
        for x, y in tuple_pop:
            population.append(code_chromosome_function(x, y))
        while t < max_iter:
            n_population = population[:]
            while len(n_population) < population_size + next_population_size:
                c1 = crossover_selection(cost_function, population, 3)
                c2 = crossover_selection(cost_function, population, 3)
                c3, c4 = single_point_crossover(c1, c2)
                mutate(c3, mut_rate)
                mutate(c4, mut_rate)
                if valid_chromosome(c3):
                    n_population.append(c3)
                if valid_chromosome(c4):
                    n_population.append(c4)
            population = sorted(n_population, key=lambda l: cost_function(l))[:population_size]
            f = cost_function(population[0])
            average_f = sum(map(cost_function, population)) / population_size
            average_list.append(average_f)
            print('Iteration:', t + 1, ', best solution:', f, ', average cost:', average_f, file=outfile)
            t += 1
            if best_f is None or best_f > f:
                best_f = f
                best = population[0]
                current_same = 0
                best_list.append(best_f)
            else:
                best_list.append(best_f)
                current_same += 1
                if current_same == convergence_number:
                    break
        all_best_lists.append(best_list)
        all_average_lists.append(average_list)
        generations_list.append(t)
        sum_cost += best_f
        sum_iterations += t
        if best_ever_f is None or best_ever_f > best_f:
            best_ever_f = best_f
            best_ever_sol = best
        print('Best solution in run', k + 1, ', composition of best chromosome', best, ', best cost',
              best_f, ', decoded best', decode_chromosome_function(best), file=outfile)
    sum_cost /= num_runs
    sum_iterations /= num_runs
    print('Average cost: %.4f' % sum_cost, file=outfile)
    print('Average number of iterations: %.2f' % sum_iterations, file=outfile)
    print('Best solution: %s' % best_ever_sol, file=outfile)
    print('Best cost: %.4f' % best_ever_f, file=outfile)
    print('Decoded best solution: %f, %f' % decode_chromosome(best_ever_sol), file=outfile)
    draw_stats(all_best_lists, all_average_lists, generations_list, population_size)


genetski()
