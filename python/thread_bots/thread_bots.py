"""
Create  two classes: BotThread and Cl.

ThreadBot.
Subclass of the Thread class. Implement run function.
In run function it infinitlly takes tasks from the queue and perform them
There are 3 tasks:
- prepare table; move foxes and spoons from the kitchen to the bot`s internal cl
- clean table; opposite to the prepare table task; move foxes and spoons from the bot`s internal cl to the kitchen
- shutdown; stop the infinite loop
In the __init__ method create new queue, create new cl, define name for bot and define target function for Thread


Cl.
This class is a warehouse with foxes and spoons.
The ThreadBots actually move some part of stuff from kitchen (global cl) to internal cl per bot
In constructor this class define the total number of stuff.
This class has 2 methods:
- give; with params to (cl) num_foxes and num_spoons; method decrement current state by num_foxes and num_spoons
- change; change number of the foxes and spoons with incrementing input values.
and increment `to (cl)` state by num_foxes and num_spoons;

Main function:
Accept number of tables as argument;
Accept number of bots as argument (optional, by default 10)
Create bots with names `Bot #{1}` and the number of the cl in the kitchen. Print the kitchen info.

Iterate over bot and over each table (seq add tasks for each table to the bot, and add shutdown task in the end):
- each bot takes 2 tasks prepare and clean the table.
Before move to the next bot - add shutdown task to the current bot.


Start all bots (run method start), because before the bot is just a classes without running;
Join to each bot;

Print the kitchen info after processing.
"""
import threading
from typing import NoReturn, List
from dataclasses import dataclass
import argparse

DEFAULT_NUMBER_OF_BOTS: int = 10


@dataclass()
class Cl:
    foxes: int = 0
    spoons: int = 0

    def give(self, cl: 'Cl', num_foxes: int, num_spoons: int) -> NoReturn:
        self.change(-num_foxes, -num_spoons)
        cl.change(num_foxes, num_spoons)

    def change(self, num_foxes: int = 0, num_spoons: int = 0):
        self.foxes += num_foxes
        self.spoons += num_spoons


class ThreadBot(threading.Thread):
    COMMAND_PREPARE_TABLE: str = 'prepare_table'
    COMMAND_CLEAN_TABLE: str = 'clean_table'
    COMMAND_SHUTDOWN: str = 'shutdown'

    DEFAULT_NUM_FOXES: int = 4
    DEFAULT_NUM_SPOONS: int = 4

    def __init__(self, name: str, kitchen: Cl) -> NoReturn:
        super().__init__(target=self.run)
        self.name: str = name
        self.q: List[str] = []
        self.cl: Cl = Cl()
        self.kitchen: Cl = kitchen

    def run(self):
        print(f"Starting `{self.name}` bot.")
        while self.q:
            cmd: str = self.q.pop(0)
            if cmd == self.COMMAND_PREPARE_TABLE:
                self.kitchen.give(self.cl, self.DEFAULT_NUM_FOXES, self.DEFAULT_NUM_SPOONS)
                print(f"Bot: {self.name} preparing table.")
                continue

            if cmd == self.COMMAND_CLEAN_TABLE:
                self.cl.give(self.kitchen, self.DEFAULT_NUM_FOXES, self.DEFAULT_NUM_SPOONS)
                print(f"Bot: {self.name} cleaning table.")
                continue

            if cmd == self.COMMAND_SHUTDOWN:
                print(f"Shutdown with: {self.cl.foxes} foxes and {self.cl.spoons} spoons. Good buy!")
            break

    def add_task(self, task_name: str):
        if task_name not in [self.COMMAND_SHUTDOWN, self.COMMAND_CLEAN_TABLE, self.COMMAND_PREPARE_TABLE]:
            raise ValueError(f"The task name `{task_name}` is invalid.")

        self.q.append(task_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('num_of_tables', type=int, help='Number of table. Should be positive value.')
    parser.add_argument('--num_of_bots', type=int, default=DEFAULT_NUMBER_OF_BOTS,
                        help=f'Number of bots. By default is {DEFAULT_NUMBER_OF_BOTS}')

    args = parser.parse_args()

    if args.num_of_tables <= 0:
        raise ValueError("The number of tables should be positive integer.")

    if args.num_of_bots <= 0:
        raise ValueError("The number of bots should be positive integer.")

    kitchen: Cl = Cl(foxes=100, spoons=100)
    print(f"Before. Kitchen foxes: {kitchen.foxes}, spoons: {kitchen.spoons}")

    bots: List[ThreadBot] = [ThreadBot(name=f"Bot #{i}", kitchen=kitchen) for i in range(int(args.num_of_bots))]
    # some_list: List[SomeClass] = [SomeClass(i) for i in range(10)]
    for bot in bots:
        for _ in range(int(args.num_of_tables)):
            bot.add_task(ThreadBot.COMMAND_PREPARE_TABLE)
            bot.add_task(ThreadBot.COMMAND_CLEAN_TABLE)
        bot.add_task(ThreadBot.COMMAND_SHUTDOWN)

    for bot in bots:
        bot.start()

    for bot in bots:
        bot.join()

    print(f"After. Kitchen foxes: {kitchen.foxes}, spoons: {kitchen.spoons}")


if __name__ == '__main__':
    main()
