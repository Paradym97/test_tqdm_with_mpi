# Parallel Progress Bar with MPI and tqdm

This is a simple function to run a function in parallel using MPI and tqdm to show the progress of the function.
The function will run on all processes and the progress bar will be updated on the root process. 

Learn from the code [with_threading.py].

## Installation

```bash
python setup.py install
```

## Usage

```python
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
```

## Example

```bash
mpirun -n 4 python example.py
```


