import math

class Vector2D:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self) -> str:
        return f"Vector2D(x={self.x:.3f}, y={self.y:.3f})"

    def __add__(self, other: "Vector2D") -> "Vector2D":
        # Vector addition: combine components
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> "Vector2D":
        # Scalar multiplication: scale magnitude
        return Vector2D(self.x * scalar, self.y * scalar)

    def magnitude(self) -> float:
        # Euclidean distance from origin
        return math.sqrt(self.x**2 + self.y**2)


class Pose2D:
    def __init__(self, x: float = 0.0, y: float = 0.0, theta: float = 0.0):
        self.position = Vector2D(x, y)
        self.theta = float(theta)  # in radians

    def __repr__(self) -> str:
        return f"Pose2D(x={self.position.x:.3f}, y={self.position.y:.3f}, theta={math.degrees(self.theta):.1f}°)"

    def update(self, v: float, omega: float, dt: float):
        """
        Updates the pose based on linear speed (v) and angular speed (omega)
        over a discrete time interval (dt).
        """
        # 1. Update orientation from angular velocity
        self.theta += omega * dt

        # 2. Normalize theta to stay strictly within [-pi, +pi]
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))

        # 3. Project linear velocity along heading into world X and Y displacements
        dx = v * math.cos(self.theta) * dt
        dy = v * math.sin(self.theta) * dt

        # 4. Update position using our Vector2D addition
        self.position = self.position + Vector2D(dx, dy)


if __name__ == "__main__":
    robot = Pose2D(x=0.0, y=0.0, theta=0.0)
    print(f"Start Pose: {robot}")

    # Drive forward and turn simultaneously (arc of a circle)
    # Linear velocity: 1.0 m/s, Angular velocity: 0.5 rad/s (~28.6 deg/s)
    dt = 0.1  # 100 ms loop step (typical in robotics)
    total_time = 10.0  # seconds
    steps = int(total_time / dt)

    for _ in range(steps):
        robot.update(v=1.0, omega=0.5, dt=dt)

    print(f"End Pose after {total_time}s: {robot}")