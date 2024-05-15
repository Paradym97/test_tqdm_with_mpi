'''
mpirun -n 4 python example.py
'''

import numpy as np
import time
from mpi4py import MPI
from tqdm_mpi import tqdm_mpi

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def main_fuc(rank=rank):
    n=np.random.randint(1, 10)
    time.sleep(rank*2+5)
    return n

ret = tqdm_mpi(comm, rank, size, main_fuc, args=(rank,),
               tqdm_kwargs={"bar_format":'{desc}: {percentage:3.0f}%|||{bar}||| {n:.1f}/{total:.1f} [{elapsed}<{remaining}]',
                            "desc": f"Process",
                            },
               )
