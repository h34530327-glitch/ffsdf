"""Simple CRUD example in Python using an in-memory repository."""

from dataclasses import dataclass, field
from typing import Dict, Iterable, Optional


@dataclass(frozen=True)
class Task:
    task_id: int
    title: str
    is_done: bool = False


@dataclass
class TaskRepository:
    _tasks: Dict[int, Task] = field(default_factory=dict)
    _next_id: int = 1

    def create(self, title: str) -> Task:
        """Create a new task and store it in the repository."""
        task = Task(task_id=self._next_id, title=title)
        self._tasks[task.task_id] = task
        self._next_id += 1
        return task

    def read(self, task_id: int) -> Optional[Task]:
        """Read a task by id."""
        return self._tasks.get(task_id)

    def list_all(self) -> Iterable[Task]:
        """List all tasks."""
        return list(self._tasks.values())

    def update(self, task_id: int, title: Optional[str] = None, is_done: Optional[bool] = None) -> Optional[Task]:
        """Update an existing task and return the updated record."""
        task = self._tasks.get(task_id)
        if task is None:
            return None

        updated_task = Task(
            task_id=task.task_id,
            title=title if title is not None else task.title,
            is_done=is_done if is_done is not None else task.is_done,
        )
        self._tasks[task_id] = updated_task
        return updated_task

    def delete(self, task_id: int) -> bool:
        """Delete a task. Returns True if the task existed."""
        return self._tasks.pop(task_id, None) is not None


def demo() -> None:
    repo = TaskRepository()

    task = repo.create("Write CRUD example")
    print("Created:", task)

    fetched = repo.read(task.task_id)
    print("Read:", fetched)

    updated = repo.update(task.task_id, is_done=True)
    print("Updated:", updated)

    repo.create("Ship documentation")
    print("All tasks:", list(repo.list_all()))

    deleted = repo.delete(task.task_id)
    print("Deleted?", deleted)
    print("Remaining:", list(repo.list_all()))


if __name__ == "__main__":
    demo()
