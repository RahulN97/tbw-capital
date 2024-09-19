import random
import time
from typing import Any, Callable, List

import pyautogui
import pytweening

from interface.screen_locator import ScreenLocator


class Controller:

    MIN_PAUSE_TIME: float = 1.0
    MAX_PAUSE_TIME: float = 1.5

    MIN_CLICK_DURATION: float = 0.1
    MAX_CLICK_DURATION: float = 0.4

    MIN_MOVE_DURATION: float = 0.2
    MAX_MOVE_DURATION: float = 1.0

    MIN_TYPE_INTERVAL: float = 0.1
    MAX_TYPE_INTERVAL: float = 0.3

    FULL_ZOOM_SCROLL_AMT: int = 30

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

    @staticmethod
    def pause_action(f: Callable) -> Callable:
        def inner(self: "Controller", *args, **kwargs) -> Any:
            if self.randomize:
                pause_time: float = random.uniform(self.MIN_PAUSE_TIME, self.MAX_PAUSE_TIME)
                time.sleep(pause_time)
            return f(self, *args, **kwargs)

        return inner

    @pause_action
    def click(
        self,
        x: int,
        y: int,
        duration: float = 0.0,
        tween: Callable[[float], float] = pytweening.linear,
    ) -> None:
        if self.randomize:
            duration = random.uniform(self.MIN_CLICK_DURATION, self.MAX_CLICK_DURATION)
            tween = random.choice(self.TWEEN_FUNCTIONS)
        pyautogui.leftClick(x=x, y=y, duration=duration, tween=tween)

    @pause_action
    def move_to(
        self,
        x: int,
        y: int,
        duration: float = 0.0,
        tween: Callable[[float], float] = pytweening.linear,
    ) -> None:
        if self.randomize:
            duration = random.uniform(self.MIN_MOVE_DURATION, self.MAX_MOVE_DURATION)
            tween = random.choice(self.TWEEN_FUNCTIONS)
        pyautogui.moveTo(x=x, y=y, duration=duration, tween=tween)

    @pause_action
    def type(self, text: str, interval: float = 0.0) -> None:
        # TODO: make sure text is not typed into chat
        if self.randomize:
            interval: float = random.uniform(self.MIN_TYPE_INTERVAL, self.MAX_TYPE_INTERVAL)
        pyautogui.write(message=text, interval=interval)

    @pause_action
    def press(self, key: str) -> None:
        pyautogui.press(key)

    @pause_action
    def hold(self, key: str, duration: float) -> None:
        with pyautogui.hold(key):
            pyautogui.sleep(duration)

    @pause_action
    def scroll(self, scroll_amt: int) -> None:
        screenWidth, screenHeight = pyautogui.size()
        self.move_to(x=screenWidth // 2, y=screenHeight // 2)
        pyautogui.scroll(scroll_amt)

    def scroll_full_zoom(self) -> None:
        self.scroll(self.FULL_ZOOM_SCROLL_AMT)

    def click_location(self, location: str) -> None:
        x, y = self.locator.get_coords(location)
        self.click(x, y)

    def click_inventory_slot(self, slot_num: int) -> None:
        x, y = self.locator.get_inv_slot_coords(slot_num)
        self.click(x, y)

    def click_ge_slot(self, slot_num: int) -> None:
        x, y = self.locator.get_ge_slot_coords(slot_num)
        self.click(x, y)

    def open_ge(self) -> None:
        self.press("esc")
        self.click_location("ge_interface")

    def exit_ge(self) -> None:
        self.press("esc")
        self.press("esc")
