def parser(method, **kwargs):
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


r = {
    "rf": None,
    "cf": None
}


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.fsize = size

    def size(self) -> int:
        return self.fsize


class Folder:
    def __init__(self, name: str, parent_folder = None):
        self.name = name
        self.files = dict()
        self.subfolders = dict()
        self.parent_folder = parent_folder

    def add_file(self, name: str, size: int):
        self.files[name] = File(name, size)

    def get_parent_folder(self):
        return self.parent_folder

    def enter_folder(self, name: str):
        if name not in self.subfolders:
            self.subfolders[name] = Folder(name, self)
        return self.subfolders[name]

    def size(self) -> int:
        return sum([sf.size() for sf in self.subfolders.values()]) + sum([f.size() for f in self.files.values()])

    def __str__(self):
        return f"{self.name} - {self.size()}"

    def __repr__(self):
        return f"{self.name}({self.size():,})"


def exec_cmd(line: str, rf: Folder, cf: Folder):
    if line.startswith("$ "):
        cmd = line[2:]
        if cmd == "cd /":
            return rf
        if cmd == "cd ..":
            return cf.get_parent_folder()
        if cmd.startswith("cd "):
            return cf.enter_folder(cmd[3:])
    elif line[0] in "123456789":
        f = line.split(" ")
        cf.add_file(f[1], int(f[0]))
    return cf


def execute_input_file(line: str, res: dict = None):
    res["cf"] = exec_cmd(line, res["rf"], res["cf"])


def get_folders_if(rf: Folder, size: int, above: bool = False) -> list:
    def gf(cf):
        if above and cf.size() >= size or \
                not above and cf.size() <= size:
            res.append(cf)
        for name, folder in cf.subfolders.items():
            gf(folder)
    res = []
    gf(rf)
    return res


if __name__ == "__main__":
    # read puzzle input, build folder struct
    r["rf"] = r["cf"] = Folder("/")
    parser(execute_input_file, res=r)

    # Answer 1
    folders = get_folders_if(r["rf"], 100000, above=False)
    size = sum([f.size() for f in folders])
    print(f"Answer1:", size, "| out of", folders)

    # Answer 2
    ocuppied = r["rf"].size()
    available = 70000000 - ocuppied
    needed = 30000000 - available
    print(f"{ocuppied=:,}\n{available=:,}\n{needed=:,}")

    folders = get_folders_if(r["rf"], needed, above=True)
    m = folders[0]
    for f in folders:
        if f.size() < m.size():
            m = f
    print("Answer2:", str(m), "| out of", folders)

