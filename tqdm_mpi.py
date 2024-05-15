from threading import Thread
from tqdm import tqdm
import time

def tqdm_mpi(comm, rank, size, function, tqdm_kwargs={}, args=[], kwargs={}):
    """
    This function is used to run a function in parallel using MPI and tqdm to show the progress of the function.
    The function will run on all processes and the progress bar will be updated on the root process.

    Args:
        comm (MPI.COMM_WORLD): The MPI communicator.
        rank (int): The rank of the current process.
        size (int): The total number of processes.
        function (function): The function to run in parallel.
        tqdm_kwargs (dict): The keyword arguments to pass to the tqdm object.
        args (list): The positional arguments to pass to the function.
        kwargs (dict): The keyword arguments to pass to the function.
    
    Returns:
        The return value of the function.

    e.g.
    from mpi4py import MPI
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
    """
    
    ret = [None]  # Mutable var so the function can store its return value
    def myrunner(function, ret, *args):
        ret[0] = function(*args)

    thread=[Thread(target=myrunner, args=(function, ret) + tuple(args), kwargs=kwargs)]
    thread[0].start()

    if rank != 0:
        while thread[0].is_alive():
            time.sleep(0.1)
        comm.send(f"Process {rank} completed", dest=0)
    else:
        pbar = tqdm(total=size, **tqdm_kwargs)
        for i in range(1, size):
            thread.append(Thread(target=comm.recv, args=(None,i)))
            thread[-1].start()
        while True:
            num = [t.is_alive() for t in thread].count(False)
            pbar.n=num
            pbar.refresh()
            if num == size:
                break
            time.sleep(0.1)
    
    return ret[0]