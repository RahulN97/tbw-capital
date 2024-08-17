import random
from typing import Callable, List

import pyautogui
import pytweening

from interface.screen_locator import ScreenLocator


class Controller:

    MAX_CLICK_DURATION: float = 0.5
    MAX_MOVE_DURATION: float = 1.5
    MAX_TYPE_INTERVAL: float = 1.0
    FULL_ZOOM_SCROLL_AMT: int = -10
    TWEEN_FUNCTIONS: List[Callable[[float], float]] = [
        pytweening.linear,
        pytweening.easeInQuad,
        pytweening.easeOutQuad,
        pytweening.easeInOutQuad,
        pytweening.easeInCubic,
        pytweening.easeOutCubic,
        pytweening.easeInOutCubic,
        pytweening.easeInElastic,
        pytweening.easeOutElastic,
        pytweening.easeInOutElastic,
        pytweening.easeInBack,
        pytweening.easeOutBack,
        pytweening.easeInOutBack,
        pytweening.easeInBounce,
        pytweening.easeOutBounce,
        pytweening.easeInOutBounce,
    ]

    def __init__(self, locator: ScreenLocator, randomize: bool) -> None:
        self.locator: ScreenLocator = locator
        self.randomize: bool = randomize

    def click(
        self,
        x: int,
        y: int,
        duration: float = 0.0,
        tween: Callable[[float], float] = pytweening.linear,
    ) -> None:
        if self.randomize:
            duration = random.uniform(0, self.MAX_CLICK_DURATION)
            tween = random.choice(self.TWEEN_FUNCTIONS)
        pyautogui.leftClick(x=x, y=y, duration=duration, tween=tween)

    def move_to(
        self,
        x: int,
        y: int,
        duration: float = 0.0,
        tween: Callable[[float], float] = pytweening.linear,
    ) -> None:
        if self.randomize:
            duration = random.uniform(0, self.MAX_MOVE_DURATION)
            tween = random.choice(self.TWEEN_FUNCTIONS)
        pyautogui.moveTo(x=x, y=y, duration=duration, tween=tween)

    def type(self, text: str, interval: float = 0.0) -> None:
        if self.randomize:
            interval: float = random.uniform(0, self.MAX_TYPE_INTERVAL)
        pyautogui.write(message=text, interval=interval)

    def press(self, key: str) -> None:
        pyautogui.press(key)

    def hold(self, key: str, duration: float) -> None:
        with pyautogui.hold(key):
            pyautogui.sleep(duration)

    def scroll(self, scroll_amt: int) -> None:
        screenWidth, screenHeight = pyautogui.size()
        self.move_to(x=screenWidth, y=screenHeight)
        pyautogui.scroll(scroll_amt)

    def click_compass(self) -> None:
        x, y = self.locator.get_coords("compass")
        self.click(x=x, y=y)

    def open_exchange(self) -> None:
        x, y = self.locator.get_coords("grand_exchange")
        self.click(x=x, y=y)

    def exit_exchange(self) -> None:
        self.press("esc")
