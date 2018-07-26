from yaml import load, dump


class LastEntry:
    def __init__(self, path: str) -> None:
        with open(path, mode="r") as file:
            data = load(file)
        self.path: str = path
        self.hh: str = data.get("hh", "")
        self.ha: int = data.get("ha", 0)
        self.hh_before: str = self.hh
        self.ha_before: int = self.ha

    def write(self):
        if (self.hh != self.hh_before) or (self.ha != self.ha_before):
            with open(self.path, mode="w") as file:
                file.write(
                    dump({
                        "hh": self.hh,
                        "ha": self.ha,
                    })
                )
