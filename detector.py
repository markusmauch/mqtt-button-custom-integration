import time
import threading
from collections import deque
from typing import Literal

SHORT_PRESS = "short_press"
DOUBLE_PRESS = "double_press"
LONG_PRESS = "long_press"
DOWN = "button_down"
UP = "button_up"

EventType = Literal[SHORT_PRESS, DOUBLE_PRESS, LONG_PRESS]

class ButtonEventsDetector:
    def __init__(self, short_press_time=0.2, long_press_time=0.8):
        self.SHORT_PRESS_time = short_press_time
        self.long_press_time = long_press_time
        self.events = deque()
        self.recording_start_time = None
        self.timer = None
        self.event_handlers = {
            SHORT_PRESS: [],
            DOUBLE_PRESS: [],
            LONG_PRESS: []
        }

    def on(self, event_type: EventType, handler):
        if event_type in self.event_handlers:
            self.event_handlers[event_type].append(handler)
        else:
            raise ValueError(f"Unknown event type: {event_type}")

    def trigger_event(self, event_type: EventType):
        for handler in self.event_handlers.get(event_type, []):
            handler()

    def now(self):
        return time.monotonic()

    def process_event(self, event_type):
        if event_type in (DOWN, UP):
            if self.recording_started() == False and event_type == DOWN:
                self.start_recording()
            self.events.append((event_type, self.now()))

    def recording_started(self):
        if self.recording_start_time is None:
            return False
        delta = self.now() - self.recording_start_time
        return delta < self.long_press_time

    def start_recording(self):
        now = self.now();
        self.recording_start_time = now
        self.timer = threading.Timer(self.long_press_time, self.analyze)
        self.timer.start()

    def analyze(self):
        result = ""
        if len(self.events) == 1 and self.events[0][0] == DOWN:
            result = LONG_PRESS
        else:
            pairs = deque()
            i = 0
            while i < len(self.events) - 1:
                event = self.events[i][0]
                if event == UP:
                    i = i + 1
                    continue
                if event == DOWN and len(self.events) > i:
                    start = self.events[i][1]
                    stop = self.events[i + 1][1]
                    if (self.events[i + 1][0] == UP):
                        pair = self.test(start, stop)
                        if (pair is not None):
                            pairs.append(pair)
                    i = i + 2
                if len(pairs) > 1:
                    break;

            if len(pairs) == 1:
                event, delta = pairs[0]
                result = event
            elif len(pairs) == 2:
                event_1, delta_1 = pairs[0]
                event_2, delta_2 = pairs[1]
                if event_1 == SHORT_PRESS and event_2 == SHORT_PRESS:
                    result = DOUBLE_PRESS

        self.timer.cancel()
        self.events.clear()
        if result != "":
            self.trigger_event(result)

    def test(self, start, stop):
        delta = stop - start
        if delta < self.SHORT_PRESS_time:
            return (SHORT_PRESS, delta)
        elif delta < self.long_press_time:
            return (LONG_PRESS, delta)