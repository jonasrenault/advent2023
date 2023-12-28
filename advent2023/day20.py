from utils.utils import Advent
from collections import defaultdict, deque
from tqdm import tqdm


advent = Advent(20)


class FlipFlop:
    def __init__(self, children) -> None:
        self.children = children
        self.on = False

    def process(self, pulse, sender):
        if pulse == "high":
            return None
        self.on = not self.on
        return [(child, "high" if self.on else "low") for child in self.children]

    def __str__(self) -> str:
        return "%" + ("on" if self.on else "off") + " -> " + ",".join(self.children)

    def __repr__(self) -> str:
        return "%" + ("on" if self.on else "off") + " -> " + ",".join(self.children)


class Broadcast:
    def __init__(self, children) -> None:
        self.children = children

    def process(self, pulse, sender):
        return [(child, pulse) for child in self.children]


class Conjunction:
    def __init__(self, children) -> None:
        self.children = children
        self.memory = {}

    def set_inputs(self, inputs):
        for input in inputs:
            self.memory[input] = "low"

    def process(self, pulse, sender):
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
        l, h = process(modules)
        low += l
        high += h

    advent.submit(1, low * high)


def process(modules):
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
        if dest in modules:
            to_send = modules[dest].process(pulse, sender)
            if to_send:
                for child, p in to_send:
                    queue.append((dest, p, child))

    return low, high


def get_modules(lines):
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
