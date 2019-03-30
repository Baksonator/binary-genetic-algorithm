import random
import sys
import math
import matplotlib.pyplot as plt
import numpy as np

max_iter = 500
mut_rate = 0.1
pop_vel = 150
npop_vel = 150
num_runs = 5
convergence_number = 10
outfile = sys.stdout


def trosak(hromozom):
    # broj razlicitih bitova
    x, y = decode_chromosome(hromozom)
    return math.fabs(mccormick_function(x, y) + 1.913)


def mutiraj(hromozom, verovatnoca):
    # inverzija
    if random.random() <= verovatnoca:
        first = random.randrange(1, len(hromozom) - 1)
        second = random.randrange(1, len(hromozom) - 1)
        if first < second:
            hromozom[first: second + 1] = reversed(hromozom[first: second + 1])
        else:
            hromozom[second: first + 1] = reversed(hromozom[second: first + 1])
    return hromozom


def code_chromosome(x, y):
    # 13 bitova po parametru
    x = int(x * 1000)
    y = int(y * 1000)
    x += 1500
    y += 3000
    hromozom_x = list(bin(x)[2:].zfill(13))
    hromozom_y = list(bin(y)[2:].zfill(13))
    return hromozom_x + hromozom_y


def decode_chromosome(chromosome):
    hromozom_x = chromosome[:13]
    hromozom_y = chromosome[13:]
    x = int(''.join(map(str, hromozom_x)), 2)
    y = int(''.join(map(str, hromozom_y)), 2)
    x -= 1500
    y -= 3000
    x /= 1000
    y /= 1000
    return x, y


def mccormick_function(x, y):
    return math.sin(x + y) + (x - y) ** 2 - 1.5 * x + 2.5 * y + 1


def valid_chromosome(chromosome):
    x, y = decode_chromosome(chromosome)
    if not (-1.5 <= x <= 4):
        return False
    if not (-3 <= y <= 4):
        return False
    return True


# turnirska selekcija - argumenti su funkcija troška, rešenje, populacija i veličina turnira
def turnir(fja, pop, vel):
    z = []
    while len(z) < vel:
        z.append(random.choice(pop))
    najbolji = None
    najbolji_f = None
    for e in z:
        ff = fja(e)
        if najbolji is None or ff < najbolji_f:
            najbolji_f = ff
            najbolji = e
    return najbolji


def ukrsti(h1, h2):
    r = random.randrange(1, len(h1) - 1)
    h3 = h1[:r] + h2[r:]
    h4 = h2[:r] + h1[r:]
    return h3, h4


def draw_stats(all_best_lists, all_average_lists):
    c = 0
    colors = ['green', 'blue', 'yellow', 'red', 'orange']
    for best_list, average_list in zip(all_best_lists, all_average_lists):
        x_number_values = best_list
        y_number_values = list(range(len(best_list)))
        p = plt.plot(x_number_values, y_number_values, linewidth=3, color=colors[c])
        plt.title('Best list', fontsize=19)
        plt.xlabel('Generations', fontsize=10)
        plt.ylabel('Function value', fontsize=10)
        plt.tick_params(axis='both', labelsize=9)
        # plt.show()
        file_name = 'best' + str(c) + '.pdf'
        # p.savefig(file_name)


def genetski():
    s_trosak = 0
    s_iteracija = 0
    best_ever_sol = None
    best_ever_f = None
    all_best_lists = []
    all_average_lists = []
    cost_function = trosak
    for k in range(num_runs):
        print('Starting: GA', k, ', population size:', pop_vel, ', maximum_iterations:', max_iter, ', mutation_rate:',
              mut_rate, ', number of runs:', num_runs, file=outfile)
        best_list = []
        average_list = []
        best = None
        best_f = None
        current_same = 0
        t = 0
        tuple_pop = zip([round(random.uniform(-1.5, 4), 3) for _ in range(pop_vel)],
                        [round(random.uniform(-3, 4), 3) for _ in range(pop_vel)])
        pop = []
        for x, y in tuple_pop:
            pop.append(code_chromosome(x, y))
        while best_f != 0 and t < max_iter:
            n_pop = pop[:]
            while len(n_pop) < pop_vel + npop_vel:
                h1 = turnir(cost_function, pop, 3)
                h2 = turnir(cost_function, pop, 3)
                h3, h4 = ukrsti(h1, h2)
                mutiraj(h3, mut_rate)
                mutiraj(h4, mut_rate)
                if valid_chromosome(h3):
                    n_pop.append(h3)
                if valid_chromosome(h4):
                    n_pop.append(h4)
            pop = sorted(n_pop, key=lambda l: cost_function(l))[:pop_vel]
            f = cost_function(pop[0])
            prosek_f = sum(map(cost_function, pop))
            average_list.append(prosek_f)
            print('Iteracija:', t, ', najbolje resenje:', f, ', prosecna prilagodjenost:', prosek_f, file=outfile)
            t += 1
            if best_f is None or best_f > f:
                best_f = f
                best = pop[0]
                current_same = 0
                best_list.append(best_f)
            else:
                best_list.append(best_f)
                current_same += 1
                if current_same == convergence_number:
                    break
        all_best_lists.append(best_list)
        all_average_lists.append(average_list)
        s_trosak += best_f
        s_iteracija += t
        if best_ever_f is None or best_ever_f > best_f:
            best_ever_f = best_f
            best_ever_sol = best
        print('Najbolje resenje u pokretanju', k, ', sastav najboljeg hromozoma', best, ', najbolji trosak',
              best_f, ', dekodovani najbolji', decode_chromosome(best), file=outfile)
    s_trosak /= num_runs
    s_iteracija /= num_runs
    print('Srednji trosak: %.2f' % s_trosak, file=outfile)
    print('Srednji broj iteracija: %.2f' % s_iteracija, file=outfile)
    print('Najbolje resenje: %s' % best_ever_sol, file=outfile)
    print('Najbolji trosak: %.2f' % best_ever_f, file=outfile)
    # draw_stats(all_best_lists, all_average_lists)


genetski()
