import time
from typing import Dict, List, Any
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing
import sysconfig
import logging
import threading
import random
from queue import Queue

logging.basicConfig(level=logging.INFO)


class Pipeline:
    def __init__(self) -> None:
        self.result: Dict[str, str] = dict()

        # self.fetch_q: Queue[str] = Queue()
        # self.proc_q: Queue[tuple[str, str]] = Queue()
        # self.store_q: Queue[tuple[str, str]] = Queue()

    def fetcher(self, task_id: str) -> str:
        """Imitation of process of downloading"""
        time.sleep(1)
        data = f"taks_id: {task_id}_{random.random()}"
        return data

    def processor(self, s: str) -> str:
        """hashing of string. Making it on CPU"""

        for _ in range(50_000):
            s = str(hash(s))

        return s

    def storer(self, key: str, val: str) -> None:
        """Save value by key"""

        self.result[key] = val

    def worker(self, task_id: str) -> None:
        """Imitation of worker"""
        string = self.fetcher(task_id)
        processed = self.processor(string)
        self.storer(task_id, processed)

    def run(self, tasks: List) -> None:
        with ThreadPoolExecutor(max_workers=5) as pool:
            pool.map(self.worker, tasks)


class SafePipeline(Pipeline):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()

    def storer(self, key: str, val: str) -> None:
        with self.lock:
            super().storer(key, val)


class AdaptivePipeline(SafePipeline):
    def get_executor(self, n: int) -> ThreadPoolExecutor | ProcessPoolExecutor:
        is_gil = sysconfig.get_config_var("Py_GIL_DISABLED") == 0

        pool = ThreadPoolExecutor(max_workers=n)

        if is_gil:
            pool = ProcessPoolExecutor(max_workers=n)
            self.result = multiprocessing.Manager().dict()

        logging.info(
            f"Pool was {'Threads' if not is_gil else 'Processes'} because gil is {is_gil}"
        )
        return pool

    def run(self, tasks: List) -> None:
        with self.get_executor(n=5) as pool:
            pool.map(self.worker, tasks)


class RobustPipeline(AdaptivePipeline):
    def worker(self, task_id: str) -> None:
        try:
            super().worker(task_id)
        except Exception as e:
            logging.error(f"Was error in worker with task_id={task_id}, error is {e}")

    def run(self, tasks: List) -> None:
        super().run(tasks)


if __name__ == "__main__":
    start = time.time()

    p = RobustPipeline()
    p.run(["12", "54", "13", 110301230123])
    print("REsult", p.result)
    end = time.time()
    print(end - start)
