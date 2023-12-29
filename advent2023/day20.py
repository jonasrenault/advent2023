from abc import ABC, abstractmethod
from collections import defaultdict, deque
from collections.abc import Iterable
from math import lcm

from tqdm import tqdm
from utils.utils import Advent

advent = Advent(20)


class Module(ABC):
    @abstractmethod
    def process(self, pulse: str, sender: str) -> list[tuple[str, str]]:
        pass


class FlipFlop(Module):
    def __init__(self, children: list[str]) -> None:
        self.children = children
        self.on = False

    def process(self, pulse: str, sender: str) -> list[tuple[str, str]]:
        if pulse == "high":
            return None
        self.on = not self.on
        return [(child, "high" if self.on else "low") for child in self.children]

    def __str__(self) -> str:
        return "%" + ("on" if self.on else "off") + " -> " + ",".join(self.children)

    def __repr__(self) -> str:
        return "%" + ("on" if self.on else "off") + " -> " + ",".join(self.children)


class Broadcast(Module):
    def __init__(self, children: list[str]) -> None:
        self.children = children

    def process(self, pulse: str, sender: str) -> list[tuple[str, str]]:
        return [(child, pulse) for child in self.children]


class Conjunction(Module):
    def __init__(self, children: list[str]) -> None:
        self.children = children
        self.memory = {}

    def set_inputs(self, inputs: Iterable[str]):
        for input in inputs:
            self.memory[input] = "low"

    def process(self, pulse: str, sender: str) -> list[tuple[str, str]]:
        self.memory[sender] = pulse
        if "low" in self.memory.values():
            send = "high"
        else:
            send = "low"
        return [(child, send) for child in self.children]

    def __str__(self) -> str:
        return (
            "&"
            + " > "
            + ", ".join(self.memory.keys())
            + "&->"
            + ", ".join(self.children)
        )

    def __repr__(self) -> str:
        return (
            "&"
            + " > "
            + ", ".join(self.memory.keys())
            + "&->"
            + ", ".join(self.children)
        )


def main():
    lines = advent.get_input_lines()
    modules = get_modules(lines)
    low = 0
    high = 0
    for i in tqdm(range(1000)):
        l, h, _ = press_btn(modules)
        low += l
        high += h
    advent.submit(1, low * high)

    # qb sends to rx, will send a low pulse when all its inputs have sent a high pulse.
    # find loops for qb's inputs sending high pulses, then get LCM
    loops = []
    for input in modules["qb"].memory.keys():
        pulse = "high"
        c = find_loops(lines, pulse, input)
        loops.append(c)
    advent.submit(2, lcm(*loops))


def find_loops(
    lines: list[str], stop_pulse: str | None = None, stop_sender: str | None = None
) -> int:
    """
    Find number of button pushes required for stop_sender to send stop_pulse

    Args:
        lines (list[str]): the problem input
        stop_pulse (str | None, optional): the pulse. Defaults to None.
        stop_sender (str | None, optional): the sender. Defaults to None.

    Returns:
        int: number of button pushes required
    """
    modules = get_modules(lines)
    c = 0
    sent = False
    while not sent:
        c += 1
        _, _, sent = press_btn(modules, stop_pulse, stop_sender)
    return c


def press_btn(
    modules: dict[str, Module],
    stop_pulse: str | None = None,
    stop_sender: str | None = None,
) -> tuple[int, int, bool]:
    """
    Press button module, sending a low pulse to broadcaster module and
    all processing all subsequent pulses. Returns the count of low and
    high pulses sent. Function will return True as third tuple element if
    stop_pulse is provided and was sent as a result of pushing the button.

    Args:
        modules (dict[str, Module]): the modules
        stop_pulse (str | None, optional): stop pulse to look for. Defaults to None.
        stop_sender (str | None, optional): sender. Defaults to None.

    Returns:
        tuple[int, int, bool]: high and low counts
    """
    queue = deque()
    queue.append(("button", "low", "broadcaster"))

    low = 0
    high = 0
    while queue:
        sender, pulse, dest = queue.popleft()
        if pulse == "high":
            high += 1
        else:
            low += 1

        if stop_pulse and pulse == stop_pulse and sender == stop_sender:
            return low, high, True

        if dest in modules:
            to_send = modules[dest].process(pulse, sender)
            if to_send:
                for child, p in to_send:
                    queue.append((dest, p, child))

    return low, high, False


def get_modules(lines: list[str]) -> dict[str, Module]:
    modules = {}
    inputs = defaultdict(set)
    for line in lines:
        children = tuple([c.strip() for c in line[line.index(">") + 1 :].split(",")])
        name = "broadcaster" if line.startswith("b") else line[1 : line.index("-") - 1]
        for child in children:
            inputs[child].add(name)
        if line.startswith("&"):
            modules[name] = Conjunction(children)
        elif line.startswith("%"):
            modules[name] = FlipFlop(children)
        else:
            modules[name] = Broadcast(children)

    for name, module in modules.items():
        if type(module) is Conjunction:
            module.set_inputs(inputs[name])

    return modules


if __name__ == "__main__":
    main()
