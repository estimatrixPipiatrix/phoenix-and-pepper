from dataclasses import dataclass, field
from enum import Enum
import heapq


class EventType(Enum):
    ORDER_PLACED = "order_placed"
    ASSIGNMENT_CHECK = "assignment_check"
    LOADING = "loading"
    SAILING = "sailing"
    ARRIVAL = "arrival"
    UNLOADING = "unloading"
    SEASON_OPENS = "season_opens"
    SEASON_CLOSES = "season_closes"


@dataclass(order=True)
class Event:
    time: float
    event_type: EventType = field(compare=False)
    agent_id: str = field(compare=False)
    metadata: dict = field(default_factory=dict, compare=False)
    sequence: int = field(default=0, compare=True)


class EventQueue:
    def __init__(self):
        self.queue = []
        self.counter = 0

    def schedule(self, event):
        event.sequence = self.counter
        self.counter += 1
        heapq.heappush(self.queue, event)

    def next(self):
        return heapq.heappop(self.queue)

    def is_empty(self):
        return len(self.queue) == 0


if __name__ == "__main__":
    q = EventQueue()
    q.schedule(
        Event(
            time=1,
            event_type=EventType.ORDER_PLACED,
            agent_id="temple",
        )
    )
    q.schedule(
        Event(
            time=3,
            event_type=EventType.SAILING,
            agent_id="ignis",
        )
    )
    q.schedule(
        Event(
            time=5,
            event_type=EventType.ARRIVAL,
            agent_id="ignis",
        )
    )

    while not q.is_empty():
        e = q.next()
        print(f"Day {e.time}: {e.event_type.value} ({e.agent_id})")
