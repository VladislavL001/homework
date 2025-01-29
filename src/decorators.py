from functools import wraps
from typing import Callable, Any, Optional

def log(filename: str="console") -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            log_massage = ""
            try:
                result = func(*args, **kwargs)
                log_massage = f'{func.__name__} ok\n'
                return result
            except Exception  as error:
                log_massage = f'{func.__name__} error: {type(error)}.\nInputs: {args}, {kwargs}'
                return ""
            finally:
                if filename == "console":
                    print (log_massage, end="\n")
                else:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(log_massage)
        return wrapper
    return decorator


@log(filename="mylog.txt")
def my_function(x: int, y:int) -> int:
    return x + y

print(my_function(1, 2))