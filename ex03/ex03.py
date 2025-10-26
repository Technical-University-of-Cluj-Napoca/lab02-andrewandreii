from datetime import datetime

class User:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"[User: {self.name}]"

colors = {"red": (0, 31), "blue": (0, 34), "gray": (1, 30), "yellow": (1, 33)}

def set_color(color_name: str):
    return f"\033[{colors[color_name][0]};{colors[color_name][1]}m"

def reset_color():
    return "\033[0m"

def smart_log(*args, **kwargs):
    level = kwargs.get("level", "debug")

    if level == "debug":
        color = "gray"
    elif level == "info":
        color = "blue"
    elif level == "warning":
        color = "yellow"
    elif level == "error":
        color = "red"
    else:
        raise ValueError("Unknown logging level")

    file = kwargs.get("save_to", None)
    file_output = file is not None

    log_str = ""

    colored = False
    if kwargs.get("color", True) is True and not file_output:
        colored = True
        log_str += set_color(color)

    if kwargs.get("timestamp", False) is True:
        log_str += datetime.now().strftime("%H:%M:%S ")

    log_str += f"[{level.upper()}] "

    log_str += "".join(map(str, args))

    if colored:
        log_str += reset_color()

    if file_output:
        with open(file, "a") as f:
            f.write(log_str)
            f.write("\n")
    else:
        print(log_str)

if __name__ == "__main__":
    user = User("Hello")
    smart_log("System started successfully!", level="info")
    smart_log("User ", user, " logging in", level="debug", timestamp=True)
    smart_log("Low disk space detected!", level="warning", save_to="system.log")
    smart_log("Model ", "training", " failed", level="error", color=True, save_to="system.log")
    smart_log("Process end", level="info", color=False)
