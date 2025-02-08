import os
from typing import Any

from src.decorators import log


def test_log_valid_input_console(capsys: Any) -> None:
    """Тестирование функции log при передаче верных данных и вывод инфы в консоль"""

    @log()
    def my_function(x: Any, y: Any) -> Any:
        return x + y

    result = my_function(1, 2)
    captured = capsys.readouterr()

    assert result == 3
    assert captured.out == "my_function ok\n"


def test_log_not_valid_input_console(capsys: Any) -> None:
    """Тестирование функции log при передаче неверных данных и вывод инфы в консоль"""

    @log()
    def my_function(x: Any, y: Any) -> Any:
        return x + y

    result = my_function(1, 2, 3, 5)
    captured = capsys.readouterr()

    assert result == ""
    assert captured.out == "my_function error: <class 'TypeError'>.\nInputs: (1, 2, 3, 5), {}"


def test_log_valid_input_file() -> None:
    """Тестирование функции log при передаче верных данных и вывод инфы в файл"""

    @log(filename="mylog.txt")
    def my_function(x: Any, y: Any) -> Any:
        return x + y

    result = my_function(1, 2)

    with open("mylog.txt", "r", encoding="utf-8") as f:
        read = f.read()

        assert result == 3
        assert read == "my_function ok\n"

    path = os.path.dirname(os.path.dirname(__file__))
    os.remove(os.path.join(path, "mylog.txt"))


def test_log_not_valid_input_file() -> None:
    """Тестирование функции log при передаче неверных данных и вывод инфы в файл"""

    @log(filename="mylog.txt")
    def my_function(x: Any, y: Any) -> Any:
        return x + y

    result = my_function(1, 2, 3, 5)

    with open("mylog.txt", "r", encoding="utf-8") as f:
        read = f.read()

        assert result == ""
        assert read == "my_function error: <class 'TypeError'>.\nInputs: (1, 2, 3, 5), {}"

    path = os.path.dirname(os.path.dirname(__file__))
    os.remove(os.path.join(path, "mylog.txt"))
