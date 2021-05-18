import numpy as np


class GA:
    def __init__(self, num_pop, cor, mr, num_epoch, num_gens, num_states):
        self.num_pop = int(num_pop)
        self.num_parents = int(self.num_pop / 2)
        self.num_offsprings = self.num_pop - self.num_parents
        self.cor = cor                                          # crossover rate
        self.mr = mr                                            # mutation rate
        self.num_epoch = num_epoch
        self.num_gens = num_gens                                # number of route blocks
        self.num_states = num_states                            # number of knapsacks

    def create_population(self):
        pop_size = (self.num_pop, self.num_gens)
        return np.random.randint(self.num_states, size=pop_size)

    def cal_fitness(self, population, model):
        fitness = [np.inf] * self.num_pop
        for i, genotype in enumerate(population):
            #print(genotype)
            fitness[i] = model.get_fitness(genotype)
        return fitness

    def selection(self, population, fitness):
        parents = np.empty(shape=(self.num_parents, self.num_gens))
        max_fitness = max(fitness)
        for i in range(self.num_parents):
            idx = np.argmin(fitness)
            parents[i, :] = population[idx, :]
            fitness[idx] = 2 * max_fitness
        return parents

    def crossover(self, parents):
        offsprings = np.empty(shape=(self.num_offsprings, self.num_gens))
        crossover_point = np.random.randint(low=1, high=self.num_gens - 1)#int(self.num_gens / 2)
        i = 0
        while i < self.num_offsprings:
            if np.random.random() < self.cor:
                continue
            idx1 = i % self.num_parents
            idx2 = (i + 1) % self.num_parents
            offsprings[i, 0:crossover_point] = parents[idx1, 0:crossover_point]
            offsprings[i, crossover_point:] = parents[idx2, crossover_point:]
            i += 1
        return offsprings

    def mutation(self, offsprings):
        mutants = np.empty(shape=(self.num_offsprings, self.num_gens))
        for i in range(self.num_offsprings):
            mutants[i, :] = offsprings[i, :]
            if np.random.random() < self.mr:
                continue
            idx = np.random.randint(self.num_gens)
            mutants[i, idx] = np.random.randint(self.num_states)
        return mutants

    def optimize(self, population, model):
        fitness_history = []
        for epoch in range(self.num_epoch):
            fitness = self.cal_fitness(population, model)
            fitness_history.append(fitness)
            parents = self.selection(population, fitness)
            offsprings = self.crossover(parents)
            mutants = self.mutation(offsprings)
            population[0:self.num_parents, :] = parents
            population[self.num_offsprings:, :] = mutants

        fitness_last_epoch = self.cal_fitness(population, model)
        idx = np.argmin(fitness_last_epoch)
        return population[idx, :], fitness_last_epoch[idx], fitness_history


if __name__ == '__main__':
    from Shift import Shift
    from Model import Model
    from Knapsacks import Employee
    model = Model()

    model.add_shift(Shift('0', '2020-01-01', '08:00:00', '13:10:00', 6.5))
    model.add_shift(Shift('1', '2020-01-01', '14:00:00', '18:34:00', 9.5))
    model.add_shift(Shift('2', '2020-01-01', '08:00:00', '14:14:00', 9.3))
    model.add_shift(Shift('3', '2020-01-01', '08:00:00', '14:14:00', 8.54))
    model.add_shift(Shift('4', '2020-01-01', '08:00:00', '14:14:00', 4.0))
    model.add_shift(Shift('5', '2020-01-01', '15:00:00', '19:30:00', 6.98))
    model.add_shift(Shift('6', '2020-01-02', '06:00:00', '17:19:00', 15.5))

    model.add_shift(Shift('8', '2020-01-02', '08:00:00', '13:10:00', 6.5))
    model.add_shift(Shift('9', '2020-01-02', '14:00:00', '18:34:00', 4.5))
    model.add_shift(Shift('10', '2020-01-03', '08:00:00', '14:14:00', 7.31))
    model.add_shift(Shift('11', '2020-01-04', '08:00:00', '14:14:00', 6.98))
    model.add_shift(Shift('12', '2020-01-05', '08:00:00', '14:14:00', 6.76))
    model.add_shift(Shift('13', '2020-01-06', '15:00:00', '19:30:00', 3.5))
    model.add_shift(Shift('14', '2020-01-07', '06:00:00', '17:19:00', 15.6))

    model.add_neighbor()


    # model.add_shift(Shift('1', '2020-01-01', '08:00:00', 6.5))
    # model.add_shift(Shift('1', '2020-01-02', '09:33:10', 5.8))
    # model.add_shift(Shift('2', '2020-01-01', '11:24:00', 9.3))
    # model.add_shift(Shift('3', '2020-01-08', '14:14:00', 2.8))
    # model.add_shift(Shift('1', '2020-01-04', '08:12:00', 10.1))
    # model.add_shift(Shift('4', '2020-01-07', '11:33:10', 7.8))
    # model.add_shift(Shift('1', '2020-01-06', '16:24:00', 2.3))
    # model.add_shift(Shift('5', '2020-01-04', '10:12:00', 11.8))
    # model.add_shift(Shift('5', '2020-01-03', '10:12:00', 4.8))
    # model.add_shift(Shift('5', '2020-01-09', '10:12:00', 7.3))
    # model.add_shift(Shift('5', '2020-01-08', '10:12:00', 10.1))
    print('Количество смен = ', model.num_shift)
    model.add_employee(Employee('1', 18, 1))
    model.add_employee(Employee('2', 14, 3))
    model.add_employee(Employee('3', 15, 2))
    model.add_employee(Employee('4', 12, 1))
    model.add_employee(Employee('5', 13, 1))
    model.add_employee(Employee('6', 13, 1))
    print('Количество людей = ', model.num_knapsacks)

    # -------------------define i/o optimizer parameters------------------- #
    num_generations = 100
    fintess_glob = np.inf
    allocation_glob = []
    fitness_history_glob = []
    num_pop = 50
    cor = 0.7
    mr = 0.3
    num_epoch = 30
    num_states = model.num_knapsacks  #количество людей
    num_gens = model.num_shift  #количество смен
    optimizer = GA(num_pop=num_pop, cor=cor, mr=mr, num_epoch=num_epoch, num_gens=num_gens, num_states=num_states)

    # -------------------optimizer running------------------- #
    for i in range(num_generations):
        population = optimizer.create_population()
        allocation, fitness, fitness_history = optimizer.optimize(population, model)
        #print('fitness', allocation, fitness, fitness_history)
        if fitness < fintess_glob:
            fintess_glob = fitness
            allocation_glob = allocation
            print(i, fintess_glob, allocation_glob)
            fitness_history_glob = fitness_history
    # -------------------optimizer running------------------- #

    # -------------------summary results------------------- #
    print('default_fitness = ', model.default_fitness)
    if fintess_glob >= model.default_fitness:
        print('Решений не найдено')
        exit(0)

    print('Результат\n',model.get_allocation_report(allocation_glob))
    # print(model.result_to_df(allocation_glob))

    from matplotlib import pyplot as plt
    fitness_history_mean = [np.mean(fitness) for fitness in fitness_history_glob]
    fitness_history_min = [np.min(fitness) for fitness in fitness_history_glob]
    plt.plot(list(range(num_epoch)), fitness_history_mean, label='Mean Fitness')
    plt.plot(list(range(num_epoch)), fitness_history_min, label='Min Fitness')
    plt.legend()
    plt.title('Fitness through the num_epoch')
    plt.xlabel('Num epoch')
    plt.ylabel('Fitness')
    plt.show()
