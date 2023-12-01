import logging
import re
import sys
from pathlib import Path

import requests

# Setup basic logging on import
LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="[advent] %(levelname)s: %(message)s"
)


# AOC server url
URL = "https://adventofcode.com/{:d}/day/{:d}/{:s}"

# Paths for inputs dir and session cookie
ROOT_DIR = Path().parent.parent.parent
INPUTS_DIR = ROOT_DIR / "inputs"
SESSION_FILE = ROOT_DIR / ".secret-session-cookie"


class Advent:
    year: int
    day: int
    session: str
    S = requests.Session()

    def __init__(self, day: int, year: int = 2023) -> None:
        """
        Save year and day and setup requests session with secret cookie.

        Args:
            day (int): the day
            year (int, optional): the year. Defaults to 2023.

        Raises:
            ValueError: if day and/or year is invalid
        """
        if not (year >= 2015 and 1 <= day <= 25):
            error = "Invalid year and/or day set."
            LOGGER.critical(error)
            raise ValueError(error)

        self.year = year
        self.day = day
        self.S.headers[
            "User-Agent"
        ] = "github.com/jonasrenault/advent2023 by jonasrenault@gmail.com"

        if SESSION_FILE.is_file():
            with open(SESSION_FILE, "r") as f:
                self.session = f.read().rstrip()
                self.S.cookies.set("session", self.session)

        if not self.session:
            error = f"Unable to read session cookie info. {SESSION_FILE.absolute()} is not a file."
            LOGGER.critical(error)
            raise ValueError(error)
        LOGGER.info("Session cookie loaded.")

    def get_input(self) -> str:
        """
        Download input for given day and year. Save it to file in INPUTS_DIR.

        Returns:
            str: the input as text
        """
        if not INPUTS_DIR.is_dir():
            INPUTS_DIR.mkdir(exist_ok=True)
            LOGGER.info(f"Created inputs directory {INPUTS_DIR.absolute()}.")

        input_file = INPUTS_DIR / "{}_{:02d}.txt".format(self.year, self.day)

        try:
            with open(input_file, "r") as f:
                input = f.read()
            LOGGER.info(f"Read input from disk for {self.year} day {self.day:02d}.")
            return input
        except FileNotFoundError:
            pass

        LOGGER.info(f"Downloading input for {self.year} day {self.day:02d}.")
        r = self.S.get(URL.format(self.year, self.day, "input"))
        res = self._check_and_get_text(r)

        with open(input_file, "w") as f:
            f.write(res)

        LOGGER.info(f"Input saved to {input_file.absolute()}.")
        return res

    def _check_and_get_text(self, r: requests.Response):
        if r.status_code != 200 or "please identify yourself" in r.text.lower():
            error = (
                f"An error occured while requesting server: {r.status_code}, {r.url}"
            )
            LOGGER.critical(error)
            LOGGER.critical(
                "Did you remember to log in and update your session cookie ?"
            )
            raise requests.HTTPError(error)
        return r.text

    def get_input_lines(self) -> list[str]:
        """
        Download input and return it as a list of lines.

        Returns:
            list[str]: the input lines
        """
        input = self.get_input()
        lines = list(map(lambda l: l.strip(), input.rstrip("\n").split("\n")))
        return lines

    def submit(self, part: int, answer) -> bool:
        """
        Submit answer for part.

        Args:
            part (int): the part
            answer (_type_): the answer

        Returns:
            bool: True if answer is correct, False otherwise.
        """
        LOGGER.info(f"Submitting answer for day {self.day:02d} PART {part}: {answer}.")

        r = self.S.post(
            URL.format(self.year, self.day, "answer"),
            data={"level": part, "answer": answer},
        )
        res = self._check_and_get_text(r).lower()
        if "did you already complete it" in res:
            LOGGER.info("Already completed or wrong day/part.")
            return False

        if "that's the right answer" in res:
            LOGGER.info("Right answer.")
            return True

        if "you have to wait" in res:
            matches = re.compile(r"you have ([\w ]+) left to wait").findall(res)
            if matches:
                LOGGER.info(f"Submitting too fast, {matches[0]} left to wait.")
            else:
                LOGGER.info(f"Submitting too fast.")
            return False

        LOGGER.info("Wrong answer.")
        return False
