import random
import logging 
import torch
from type_system import STRING, Type, List, INT, BOOL
from cons_list import tuple2constlist

class Dataset(torch.utils.data.IterableDataset):
    """
        Dataset as an iterator: gives a stream of tasks
        a task is (IOs, program)

        size: size of the dataset

        nb_inputs_max: number of IOs in a task
        arguments: list of arguments for the program

        size_max: maximum number of elements in a list
        lexicon: possible values in a list
    """
    def __init__(self, 
        size, 
        dsl, 
        pcfg, 
        nb_inputs_max, 
        arguments,
        # IOEncoder,
        # IOEmbedder,
        ProgramEncoder,
        size_max,
        lexicon,
        ):
        super(Dataset).__init__()
        self.size = size
        self.dsl = dsl
        self.pcfg = pcfg
        self.input_sampler = Input_sampler(size_max = size_max, lexicon = lexicon)
        self.program_sampler = pcfg.sampling()
        self.nb_inputs_max = nb_inputs_max
        self.arguments = arguments
        # self.IOEncoder = IOEncoder
        # self.IOEmbedder = IOEmbedder
        self.ProgramEncoder = ProgramEncoder
        self.lexicon = lexicon

    def __iter__(self):
        return (self.__single_data__() for i in range(self.size))

    def __single_data__(self):
        # print("generating...")
        flag = True
        output = None
        while flag or output == None:
            program = next(self.program_sampler)
            while program.is_constant():
                program = next(self.program_sampler)
            nb_IOs = random.randint(1, self.nb_inputs_max)
            inputs = [[self.input_sampler.sample(type_) for type_ in self.arguments] for _ in range(nb_IOs)]
            try:
                outputs = []
                for input_ in inputs:
                    environment = tuple2constlist(input_)
                    output = program.eval_naive(self.dsl, environment)
                    if self.__output_validation__(output):
                        outputs.append(output)
                    else:
                        raise ValueError()
                flag = False
            except:
                pass
        
        # print("\tprogram:", program)
        IOs = [[I,O] for I,O in zip(inputs, outputs)]
        logging.debug('Found a program:\n{}\nand inputs:\n{}'.format(program,IOs))
        return IOs, self.ProgramEncoder(program), program
        # return self.IOEncoder.encode_IOs(IOs), self.ProgramEncoder(program)
    


    def __output_validation__(self, output):
        if len(output) == 0 or len(output) > self.input_sampler.size_max: 
            return False
        for e in output:
            if e not in self.lexicon:
                return False
        return True

class Input_sampler():
    """
    Object to sample element of a given type together with constraints parameters 
    For now we can only sample from the base types string, int and bool. And any list types that is based on lists or base types.
    However we sample elements from a lexicon so we cannot sample both a int list and a string for example sincei nthat case the lexicon woul need to conatin integers and strings.

    size_max: max number of elements in an input 
    lexicon: admissible elements in a list
    """
    def __init__(self, size_max, lexicon) -> None:
        self.size_max = size_max
        self.lexicon = lexicon

    def sample(self, type: Type):
        if isinstance(type, List):
            size = random.randint(1, self.size_max)
            res = [self.sample(type.type_elt) for _ in range(size)]
            return res
        if type.__eq__(INT):
            return random.choice(self.lexicon)
        elif type.__eq__(STRING):
            size = random.randint(1, self.size_max)
            res = "".join([random.choice(self.lexicon) for _ in range(size)])
            return res
        elif type.__eq__(BOOL):
            return random.random() > .5
        assert(False)

