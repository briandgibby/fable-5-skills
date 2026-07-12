from src.defaults import DEFAULTS


class RelayClient:
    def __init__(self):
        self.timeout = DEFAULTS["request_timeout_seconds"]
        self.retries = DEFAULTS["retries"]
        self.user_agent = DEFAULTS["user_agent"]

    def describe(self):
        return (
            f"RelayClient(timeout={self.timeout}s, "
            f"retries={self.retries}, user_agent={self.user_agent})"
        )


if __name__ == "__main__":
    print(RelayClient().describe())
