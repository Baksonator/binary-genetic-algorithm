import random
import sys
import math

max_iter = 500
mut_rate = 0.1

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
            hromozom[first : second + 1] = reversed(hromozom[first : second + 1])
        else:
            hromozom[second : first + 1] = reversed(hromozom[second : first + 1])
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
    x = int(''.join(map(str, hromozom_x)))
    y = int(''.join(map(str, hromozom_y)))
    x -= 1500
    y -= 3000
    x /= 1000
    y /= 1000
    print(x)
    print(y)
    return x, y

def mccormick_function(x, y):
    return math.sin(x + y) + (x - y) ** 2 - 1.5 * x + 2.5 * y + 1

def valid_chromosome(chromosome):
    x, y = decode_chromosome(chromosome)
    if not (x >= -1.5 and x <= 4):
        return False
    if not (y >= -3 and y <= 4):
        return False
    return True

def genetski():
    pop_vel = 10
    npop_vel = 10

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

    # jednotačkasto ukrštanje hromozoma
    def ukrsti(h1, h2):
        r = random.randrange(1, len(h1) - 1)
        h3 = h1[:r] + h2[r:]
        h4 = h2[:r] + h1[r:]
        return h3, h4

    #    outfile = codecs.open('izlaz_ga.txt', 'w', 'utf-8')
    outfile = sys.stdout

    # test (traženo rešenje) prevodimo u kodovani oblik
    test_d = code_chromosome(-0.547, -1.547)
    # veličina testa
    s_trosak = 0
    s_iteracija = 0
    best_ever_sol = None
    best_ever_f = None
    # 5 pokretanja genetskog algoritma
    for k in range(5):
        print('Pokretanje: GA', test_d, mut_rate, k, file=outfile)
        #                print('Pokretanje: GA', test, test_d, alfnaziv, mut_rat, k)
        best = None
        best_f = None
        t = 0
        # generisanje populacije pomoću alfabeta
        # pop = [[random.choice([0, 1]) for i in range(test_vel)] for j in range(pop_vel)]
        tuple_pop = zip([round(random.uniform(-1.5, 4), 3) for i in range(pop_vel)],
                        [round(random.uniform(-3, 4), 3) for i in range(pop_vel)])
        # pop = [code_chromosome(x, y) for x, y in tuple_pop]
        pop = []
        for x, y in tuple_pop:
            pop.append(code_chromosome(x, y))
        # ponavljamo dok ne postignemo maksimum iteracija ili dok trošak ne postane 0
        while best_f != 0 and t < max_iter:
            n_pop = pop[:]
            while len(n_pop) < pop_vel + npop_vel:
                h1 = turnir(trosak, pop, 3)
                h2 = turnir(trosak, pop, 3)
                h3, h4 = ukrsti(h1, h2)
                mutiraj(h3, mut_rate)
                mutiraj(h4, mut_rate)
                if valid_chromosome(h3):
                    n_pop.append(h3)
                    # print("Dodajem")
                if valid_chromosome(h4):
                    n_pop.append(h4)
                    # print("Dodajem")
            pop = sorted(n_pop, key=lambda x: trosak(x))[:pop_vel]
            f = trosak(pop[0])
            # print("Evo me")
            if best_f is None or best_f > f:
                best_f = f
                best = pop[0]
            #                    print(t, best_f, file=outfile)
            t += 1
        s_trosak += best_f
        s_iteracija += t
        # ako smo našli bolji od prethodnog, ažuriramo najbolje rešenje
        if best_ever_f is None or best_ever_f > best_f:
            best_ever_f = best_f
            best_ever_sol = best
        print("Najbolje resenje u pokretanju", t, best, best_f, file=outfile)
    #                print(t, best, best_f)
    # na kraju svih izvršavanja izračunavamo srednji trošak i srednji broj iteracija
    s_trosak /= 5
    s_iteracija /= 5
    print('Srednji trosak: %.2f' % s_trosak, file=outfile)
    print('Srednji broj iteracija: %.2f' % s_iteracija, file=outfile)
    print('Najbolje resenje: %s' % best_ever_sol, file=outfile)
    print('Najbolji trosak: %.2f' % best_ever_f, file=outfile)

genetski()