from cons_list import cons_list2list
import typing
import ray
from ray.util.queue import Empty
import tqdm
from pcfg import PCFG
import logging
from program import BasicPrimitive, Function, New, Program, Variable
import time
from typing import Callable, Tuple
import grammar_splitter
from Algorithms.ray_parallel import start, make_parallel_pipelines

from Algorithms.heap_search import heap_search
from Algorithms.heap_search_naive import heap_search_naive
from Algorithms.a_star import a_star
from Algorithms.threshold_search import threshold_search
from Algorithms.dfs import dfs
from Algorithms.bfs import bfs
from Algorithms.sort_and_add import sort_and_add
from Algorithms.sqrt_sampling import sqrt_sampling, sqrt_sampling_with_sbsur

from program_as_list import reconstruct_from_compressed

logging_levels = {0: logging.INFO, 1: logging.DEBUG}


verbosity = 0
logging.basicConfig(format='%(message)s', level=logging_levels[verbosity])
timeout = 100
total_number_programs = 1_000_000

list_algorithms = [
    (heap_search, 'heap search', {}),
    (sqrt_sampling, 'SQRT', {}),
    (sqrt_sampling_with_sbsur, 'SQRT+SBS UR', {}),
    (threshold_search, 'threshold', {'initial_threshold' : 0.0001, 'scale_factor' : 10}),
    (bfs, 'bfs', {'beam_width' : 5e5}),
    (dfs, 'dfs', {}),
    (sort_and_add, 'sort and add', {}),
    (a_star, 'A*', {}),
    # (heap_search_naive, 'heap search naive', {}),
]
# Set of algorithms where we need to reconstruct the programs
reconstruct = {dfs, bfs, threshold_search, a_star,
               sort_and_add, sqrt_sampling_with_sbsur}


def run_algorithm(is_correct_program: Callable[[Program], bool], pcfg: PCFG, algo_index: int) -> Tuple[Program, float, float, int, float, float]:
    '''
    Run the algorithm until either timeout or 1M programs, and for each program record probability and time of output
    return program, search_time, evaluation_time, nb_programs, cumulative_probability, probability
    '''
    algorithm, name_algo, param = list_algorithms[algo_index]
    search_time = 0
    evaluation_time = 0
    gen = algorithm(pcfg, **param)
    found = False
    if name_algo == "SQRT":
        _ = next(gen)
    nb_programs = 0
    cumulative_probability = 0

    while (search_time + evaluation_time < timeout and nb_programs < total_number_programs):

        # Searching for the next program
        search_time -= time.perf_counter()
        try:
            program = next(gen)
        except:
            search_time += time.perf_counter()
            logging.debug(
                "Output the last program after {}".format(nb_programs))
            break  # no next program

  
        search_time += time.perf_counter()
        # logging.debug('program found: {}'.format(program))

        if program == None:
            logging.debug(
                "Output the last program after {}".format(nb_programs))
            break

        nb_programs += 1
        # Reconstruction if needed
        if algorithm in reconstruct:
            target_type = pcfg.start[0]
            program_r = reconstruct_from_compressed(program, target_type)
            probability = pcfg.probability_program(pcfg.start, program_r)
        else:
            probability = pcfg.probability_program(pcfg.start, program)
            program_r = program

        cumulative_probability += probability
        # logging.debug('probability: %s' %
        #               probability)

        # Evaluation of the program
        evaluation_time -= time.perf_counter()
        found = is_correct_program(program_r)
        evaluation_time += time.perf_counter()

        if nb_programs % 100_000 == 0:
            logging.debug('tested {} programs'.format(nb_programs))

        if found:
            # logging.debug("\nSolution found: %s" % program)
            # logging.debug('[NUMBER OF PROGRAMS]: %s' % nb_programs)
            # logging.debug("[SEARCH TIME]: %s" % search_time)
            # logging.debug("[EVALUATION TIME]: %s" % evaluation_time)
            # logging.debug("[TOTAL TIME]: %s" % (evaluation_time + search_time))
            return program, search_time, evaluation_time, nb_programs, cumulative_probability, probability

    # logging.debug("\nNot found")
    # logging.debug('[NUMBER OF PROGRAMS]: %s' % nb_programs)
    # logging.debug("[SEARCH TIME]: %s" % search_time)
    # logging.debug("[EVALUATION TIME]: %s" % evaluation_time)
    # logging.debug("[TOTAL TIME]: %s" % (evaluation_time + search_time))
    return None, search_time, evaluation_time, nb_programs, cumulative_probability, probability

def insert_prefix(prefix, prog):
    try:
        head, tail = prog
        return (head, insert_prefix(prefix, tail))
    except:
        return prefix


def reconstruct_from_list(program_as_list, target_type):
    if len(program_as_list) == 1:
        return program_as_list.pop()
    else:
        P = program_as_list.pop()
        if isinstance(P, (New, BasicPrimitive)):
            list_arguments = P.type.ends_with(target_type)
            arguments = [None] * len(list_arguments)
            for i in range(len(list_arguments)):
                arguments[len(list_arguments) - i - 1] = reconstruct_from_list(
                    program_as_list, list_arguments[len(
                        list_arguments) - i - 1]
                )
            return Function(P, arguments)
        if isinstance(P, Variable):
            return P
        assert False


def insert_prefix_toprog(prefix, prog, target_type):
    prefix = cons_list2list(prefix)
    return reconstruct_from_list([prog] + prefix, target_type)

def run_algorithm_parallel(is_correct_program: Callable[[Program], bool], pcfg: PCFG, algo_index: int, splits: int,
                           n_filters: int = 4, transfer_queue_size: int = 500_000, transfer_batch_size: int = 10) -> Tuple[Program, float, typing.List[float], typing.List[float], typing.List[int], typing.List[float], float]:
    '''
    Run the algorithm until either timeout or 1M programs, and for each program record probability and time of output
    return program, search_time, evaluation_time, nb_programs, cumulative_probability, probability
    '''
    algorithm, _, param = list_algorithms[algo_index]

    @ray.remote
    class DataCollectorActor:
        def __init__(self, n_filters, n_producers):
            self.search_times = [0] * n_producers
            self.probabilities = [0] * n_producers
            self.generated_programs = [0] * n_producers
            self.evaluations_times = [0] * n_filters
            self.evaluated_programs = [0] * n_filters
            self.programs = 0

        def add_search_data(self, index, t, probability) -> bool:
            self.search_times[index] += t
            self.probabilities[index] += probability
            self.generated_programs[index] += 1
            if self.search_times[index] > timeout:
                return True
            if self.programs > total_number_programs:
                return True

            return False

        def add_evaluation_data(self, index, t):
            self.evaluations_times[index] += t
            self.evaluated_programs[index] += 1
            self.programs += 1

        def search_data(self):
            return self.search_times, self.probabilities, self.generated_programs

        def evaluation_data(self):
            return self.evaluations_times, self.evaluated_programs

    data_collector = DataCollectorActor.remote(n_filters, splits)

    def bounded_generator(prefix, cur_pcfg, i):
        if algorithm in reconstruct:
            def new_gen():
                gen = algorithm(cur_pcfg, **param)
                target_type = pcfg.start[0]
                try:
                    while True:
                        t = -time.perf_counter()
                        p = next(gen)
                        prog = insert_prefix(prefix, p)
                        t += time.perf_counter()
                        prog_r = reconstruct_from_compressed(prog, target_type)
                        probability = pcfg.probability_program(pcfg.start, prog_r)
                        if ray.get(data_collector.add_search_data.remote(i, t, probability)):
                            break
                        yield prog_r
                except StopIteration:
                    return
        else:
            def new_gen():
                gen = algorithm(cur_pcfg)
                target_type = pcfg.start[0]
                try:
                    while True:
                        t = -time.perf_counter()
                        p = next(gen)
                        if prefix is None:
                            prog = p
                            t += time.perf_counter()
                        else:
                            prog = insert_prefix_toprog(prefix, p, pcfg.start[0])
                            t += time.perf_counter()

                        if prog is None:
                            continue
                        # print(f"Generated:", prog)
                        # break
                        probability = pcfg.probability_program(
                            pcfg.start, prog)
                        if ray.get(data_collector.add_search_data.remote(i, t, probability)):
                            break
                        yield prog
                except StopIteration:
                    return
        return new_gen
    
    grammar_split_time = - time.perf_counter()
    splits = grammar_splitter.split(pcfg, splits, alpha=1.05)
    grammar_split_time += time.perf_counter() 
    make_generators = [bounded_generator(
            prefix, pcfg, i) for i, (prefix, pcfg) in enumerate(splits)]

    def make_filter(i):
        def evaluate(program):
            t = -time.perf_counter()
            found = is_correct_program(program)
            t += time.perf_counter()
            data_collector.add_evaluation_data.remote(i, t)
            return found
        return evaluate

    producers, filters, transfer_queue, out = make_parallel_pipelines(
        make_generators, make_filter, n_filters, transfer_queue_size, splits, transfer_batch_size)
    start(filters)
    logging.debug("\tStarted {} filters.".format(len(filters)))
    start(producers)
    logging.debug("\tStarted {} producers.".format(len(producers)))

    found = False
    while not found:
        try:
            program = out.get(timeout=2)
            found = True
        except Empty:
            pass
        search_times, cumulative_probabilities, nb_programs = ray.get(
            data_collector.search_data.remote())
        if sum(nb_programs) > total_number_programs:
            break

    logging.debug(
        "\tFinished search found={}. Now shutting down...".format(found))
    search_times, cumulative_probabilities, nb_programs = ray.get(data_collector.search_data.remote())
    evaluation_times, evaluated_programs = ray.get(data_collector.evaluation_data.remote())
    logging.info(
        "\tStats: found={} generated programs={} evaluated programs={} covered={:.1f}%".format(found, sum(nb_programs), sum(evaluated_programs), 100*sum(cumulative_probabilities)))
        
    # Shutdown
    for producer in producers:
        try:
            ray.kill(producer)
        except ray.exceptions.RayActorError:
            continue
    for filter in filters:
        try:
            ray.kill(filter)
        except ray.exceptions.RayActorError:
            continue
    transfer_queue.shutdown(True)
    out.shutdown(True)

    logging.info("\tShut down.")


    if found:
        probability = pcfg.probability_program(pcfg.start, program)
        return program, grammar_split_time, search_times, evaluation_times, nb_programs, cumulative_probabilities, probability
    return None, grammar_split_time, search_times, evaluation_times, nb_programs, cumulative_probabilities, 0


def gather_data(dataset: typing.List[Tuple[str, PCFG, Callable]], algo_index: int) -> typing.List[Tuple[str, Tuple[Program, float, float, int, float, float]]]:
    algorithm, _, _ = list_algorithms[algo_index]
    logging.info('\n## Running: %s' % algorithm.__name__)
    output = []
    successes = 0
    pbar = tqdm.tqdm(total=len(dataset))
    pbar.set_postfix_str(f"{successes} solved")
    for task_name, pcfg, is_correct_program in dataset:
        logging.debug("## Task:", task_name)
        data = run_algorithm(is_correct_program, pcfg, algo_index)
        successes += data[0] is not None
        output.append((task_name, data))
        pbar.update(1)
        pbar.set_postfix_str(f"{successes} solved")
    return output


def gather_data_parallel(dataset: typing.List[Tuple[str, PCFG, Callable]], algo_index: int, splits: int, n_filters: int = 4, transfer_queue_size: int = 500_000, transfer_batch_size: int = 10) -> typing.List[Tuple[str, Tuple[Program, float, typing.List[float], typing.List[float], typing.List[int], typing.List[float], float]]]:
    algorithm, _, _ = list_algorithms[algo_index]
    logging.info('\n## Running: %s with %i CPUs' % (algorithm.__name__, splits))
    output = []
    pbar = tqdm.tqdm(total=len(dataset))
    successes = 0
    pbar.set_postfix_str(f"{successes} solved")

    for task_name, pcfg, is_correct_program in dataset:
        logging.debug("## Task:", task_name)
        data = run_algorithm_parallel(
            is_correct_program, pcfg, algo_index, splits, n_filters, transfer_queue_size, transfer_batch_size)
        output.append((task_name, data))
        successes += data[0] is not None
        pbar.update(1)
        pbar.set_postfix_str(f"{successes} solved")
    return output
