from enum import Enum

from base import BaseSolution


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @property
    def move_action(self):
        if self is Direction.NORTH:
            return "N"
        elif self is Direction.EAST:
            return "E"
        elif self is Direction.SOUTH:
            return "S"
        elif self is Direction.WEST:
            return "W"

    def turned_by(self, degrees):
        return Direction((self.value * 90 + degrees) % 360 // 90)


class Ship:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = Direction.EAST
        self.waypoint_x = 10
        self.waypoint_y = 1

    def navigate(self, action, value):
        if action == "N":
            self.y += value
        elif action == "S":
            self.y -= value
        elif action == "E":
            self.x += value
        elif action == "W":
            self.x -= value
        elif action == "L":
            self.direction = self.direction.turned_by(-value)
        elif action == "R":
            self.direction = self.direction.turned_by(value)
        elif action == "F":
            self.navigate(self.direction.move_action, value)
        else:
            raise Exception(f"Unknown action: {action}")

    def navigate_waypoint(self, action, value):
        if action == "N":
            self.waypoint_y += value
        elif action == "S":
            self.waypoint_y -= value
        elif action == "E":
            self.waypoint_x += value
        elif action == "W":
            self.waypoint_x -= value
        elif action == "L":
            self.navigate_waypoint("R", -value)
        elif action == "R":
            for _ in range(value % 360 // 90):
                self.waypoint_x, self.waypoint_y = self.waypoint_y, -self.waypoint_x
        elif action == "F":
            self.x += value * self.waypoint_x
            self.y += value * self.waypoint_y

    @property
    def distance(self):
        return abs(self.x) + abs(self.y)


class Solution(BaseSolution):
    def load_data(self, input):
        return [(line[0], int(line[1:])) for line in input.splitlines()]

    def part1(self, data):
        ship = Ship()
        for action, value in data:
            ship.navigate(action, value)
        return ship.distance

    def part2(self, data):
        ship = Ship()
        for action, value in data:
            ship.navigate_waypoint(action, value)
        return ship.distance
