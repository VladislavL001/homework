import pytest
from src.processing import filter_by_state, sort_by_date

@pytest.fixture
def date_records():
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    ]

@pytest.mark.parametrize(
    "state, example",
    [
        (
            "CANCELED",
            [
                {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
            ],
        ),
        (
            "error",
            []
        ),
    ]
)
def test_filter_by_state(date_records, state, example):
    assert filter_by_state(date_records, state) == example


@pytest.fixture
def date_records():
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 124567890, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
    ]

def test_sort_by_date_ascending(date_records):
    sorted_records = sort_by_date(date_records, descending=False)
    assert sorted_records[0]['date'] == '2018-06-30T02:08:58.425572'
    assert sorted_records[-1]['date'] == '2019-07-03T18:35:29.512364'


def test_sort_by_date_descending(date_records):
    sorted_records = sort_by_date(date_records, descending=True)
    assert sorted_records[0]['date'] == '2019-07-03T18:35:29.512364'
    assert sorted_records[-1]['date'] == '2018-06-30T02:08:58.425572'



