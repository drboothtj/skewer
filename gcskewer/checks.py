'''
checks inputs for gcskewer
    classes:
        GCSkewerError(Exception)
        InputError(GCSkewerError)
    functions:
        check_input(args)
        check_output(args)
        get_window_size(sequences: List) -> int
        get_step_size(window_size: int) -> int
        check_window_and_step(window_size, step_size, sequences) -> (int, int)
'''
from typing import List
from gcskewer.io import print_to_system

class GCSkewerError(Exception):
    '''
    General error for gcskewer
    '''

class InputError(GCSkewerError):
    '''
    Error raised for incorrectly provided inputs
    '''

def check_input(args):
    '''
    Checks what input the user provided, and
    errors if neither or both is set, or
    returns file type for reading
        arguments:
            args: args from argsparse
        returns:
            input path, file extension

    '''
    if args.genbank is None and args.fasta is None:
        raise InputError('No input file! Please specify a genbank or fasta file.')
    if args.fasta and args.genbank:
        raise InputError('Both genbank and fasta input provided - pick one!')
    if args.genbank is None:
        return args.fasta, 'fasta'
    if args.fasta is None:
        return args.genbank, 'genbank'
    raise InputError(
        'Something unexpected happened when processing the input. Please contact directly for help!'
        )

def check_output(args):
    '''
        checks if any output is asked for
        arguments:
            args: args from argsparse
        returns:
            None
    '''
    if (args.csv or args.svg or args.plot) is False:
        raise InputError(
        'No output specified. Please specify at least one output format.'
        )

def get_window_size(sequences: List) -> int:
    '''
    return window size of 1% of the smalles sequences
        arguments:
            record_sequences: list of dna sequences
        returns:
            window_size: 1% of the smallest sequence
    '''
    sequence_lengths = [len(seq) for seq in sequences]
    window_size = min(sequence_lengths) // 100
    return window_size

def get_step_size(window_size: int) -> int:
    '''
    returns 1/10 of the window size
        arguments:
            window_size: window size for analysis
        returns:
            step_size: step size is 1/10 of the window size
    '''
    step_size = window_size // 10
    return step_size

def check_window_and_step(window_size, step_size, sequences) -> (int, int):
    '''
    checks if window and step sizes are set and, 
    if not, automatically sets them proportionate to the size of the smallest input sequence
        arguments:
            window_size: window size from argparse
            step_size: step size from argparse
            sequences: a list of input dna sequences
    '''
    if window_size is None:
        window_size = get_window_size(sequences)
        print_to_system(
            'Warning: No window size provided. Automatically set to: ' + str(window_size)
            )
    if step_size is None:
        step_size = get_step_size(window_size)
        print_to_system('Warning: No step size provided. Automatically set to: ' + str(step_size))
    return window_size, step_size
