
class Version:
    def __init__(self, major: int, minor: int, build: int, revision: int) -> None:
        self.major: int = major
        self.minor: int = minor
        self.build: int = build
        self.revision: int = revision
        self.version_tuple: tuple = (major, minor, build, revision)

    def __gt__(self, other) -> bool:
        return self.version_tuple > other.version_tuple

    def __ge__(self, other) -> bool:
        return self.version_tuple >= other.version_tuple

    def __lt__(self, other) -> bool:
        return self.version_tuple < other.version_tuple

    def __le__(self, other) -> bool:
        return self.version_tuple <= other.version_tuple

    def __eq__(self, other) -> bool:
        return self.version_tuple == other.version_tuple

    @staticmethod
    def from_string(version: str):
        version_array: list = version.split(".")

        if len(version_array) != 4:
            raise Exception("Invalid version string: " + version)

        return Version(*tuple(map(int, version_array)))
