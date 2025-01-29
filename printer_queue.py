from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Optimizes 3D print queue according to printer priorities and constraints
    :param print_jobs: List of print jobs
    :param constraints: Printer constraints
    :return: Dict with ordered jobs IDs and total print time
    """
    print_jobs = [PrintJob(**job) for job in print_jobs]
    constraints = PrinterConstraints(**constraints)

    n = len(print_jobs)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if print_jobs[j].priority > print_jobs[j + 1].priority:
                print_jobs[j], print_jobs[j + 1] = print_jobs[j + 1], print_jobs[j]

    print_order = []
    total_time = 0

    while print_jobs:
        current_batch = []
        batch_volume = 0

        for job in print_jobs[:]:
            if len(current_batch) < constraints.max_items and batch_volume + job.volume <= constraints.max_volume:
                current_batch.append(job)
                batch_volume += job.volume

        for job in current_batch:
            print_jobs.remove(job)

        if current_batch:
            print_order.extend([job.id for job in current_batch])
            total_time += max(job.print_time for job in current_batch)

    return {"print_order": print_order, "total_time": total_time}


def test_printing_optimization():
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
    ]

    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Test 1 (Same priority tasks):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Print order: {result1['print_order']}")
    print(f"Total time: {result1['total_time']} min")

    print("\nTest 2 (Different priorities):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Print order: {result2['print_order']}")
    print(f"Total time: {result2['total_time']} min")

    print("\nTest 3 (Exceeding constraints):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Print order: {result3['print_order']}")
    print(f"Total time: {result3['total_time']} min")


if __name__ == "__main__":
    test_printing_optimization()
