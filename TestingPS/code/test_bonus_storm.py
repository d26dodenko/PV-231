from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from django.test import RequestFactory

from apps.games import views
from apps.games.forms import SlotBetForm

NO_WIN = (Decimal("0"), None, 0)


@pytest.mark.parametrize(
    ("bet", "error_code"),
    [
        pytest.param("1.99", "min_value", id="TC-01"),
        pytest.param("2.00", None, id="TC-02"),
        pytest.param("100000.00", None, id="TC-03"),
        pytest.param("100000.01", "max_value", id="TC-04"),
        pytest.param("2.001", "max_decimal_places", id="TC-05"),
        pytest.param("abc", "invalid", id="TC-06"),
        pytest.param("", "required", id="TC-07"),
    ],
)
def test_bet_limits(bet, error_code):
    form = SlotBetForm({"bet": bet})

    if error_code is None:
        assert form.is_valid()
        assert form.cleaned_data["bet"] == Decimal(bet)
    else:
        assert not form.is_valid()
        assert form.errors.as_data()["bet"][0].code == error_code


@pytest.mark.parametrize(
    ("symbols", "bet", "expected"),
    [
        pytest.param("LOW1 LOW1 LOW2 LOW1 LOW1", "10", NO_WIN, id="TC-08"),
        pytest.param("LOW1 LOW1 LOW1 LOW2 LOW1", "10", (Decimal("2.10"), "LOW1", 3), id="TC-09"),
        pytest.param("LOW1 LOW1 LOW1 LOW1 LOW2", "10", (Decimal("5.60"), "LOW1", 4), id="TC-10"),
        pytest.param("HIGH3 HIGH3 HIGH3 HIGH3 HIGH3", "10", (Decimal("700.00"), "HIGH3", 5), id="TC-11"),
        pytest.param("WILD HIGH2 WILD HIGH2 LOW1", "10", (Decimal("84.00"), "HIGH2", 4), id="TC-12"),
        pytest.param("WILD WILD WILD WILD WILD", "10", (Decimal("1400.00"), "WILD", 5), id="TC-13"),
        pytest.param("LOW1 LOW1 SCATTER LOW1 LOW1", "10", NO_WIN, id="TC-14"),
        pytest.param("LOW1 LOW1 LOW1 SCATTER LOW1", "10", (Decimal("2.10"), "LOW1", 3), id="TC-15"),
        pytest.param("LOW1 LOW1 LOW1 LOW2 LOW2", "2.50", (Decimal("0.52"), "LOW1", 3), id="TC-16"),
        pytest.param("UNKNOWN UNKNOWN UNKNOWN LOW1 LOW2", "10", NO_WIN, id="TC-17"),
    ],
)
def test_line_payout(symbols, bet, expected):
    assert views._line_payout(symbols.split(), Decimal(bet)) == expected


def make_grid(scatter_positions):
    grid = [
        [symbol] * 3 for symbol in ("LOW1", "LOW2", "MID1", "MID2", "MID3")
    ]
    for reel, row in scatter_positions:
        grid[reel - 1][row - 1] = "SCATTER"
    return grid


@pytest.mark.parametrize(
    ("scatter_positions", "expected"),
    [
        pytest.param(((1, 1), (3, 2), (5, 3)), True, id="TC-18"),
        pytest.param(((1, 1), (3, 2)), False, id="TC-19"),
        pytest.param(((1, 1), (2, 2), (5, 3)), False, id="TC-20"),
        pytest.param(((1, 1), (1, 2), (1, 3)), False, id="TC-21"),
    ],
)
def test_scatter_trigger(scatter_positions, expected):
    assert views._scatter_triggered(make_grid(scatter_positions)) is expected


@pytest.fixture
def play_spin(monkeypatch):
    def play(grid, free_spins):
        player = SimpleNamespace(balance=Decimal("200.00"), free_spins_bonus=free_spins, save=Mock())
        request = RequestFactory().post("/bonus-storm/", {"bet": "5.00"})
        request.user = SimpleNamespace(is_authenticated=True, player_profile=player)
        game = object()
        session = SimpleNamespace(save=Mock())

        monkeypatch.setattr(views.Game.objects, "get", Mock(return_value=game))
        monkeypatch.setattr(views.GameSession.objects, "create", Mock(return_value=session))
        monkeypatch.setattr(views.Transaction.objects, "create", Mock())
        monkeypatch.setattr(views, "apply_bet", Mock())
        monkeypatch.setattr(views, "apply_win", Mock())
        monkeypatch.setattr(views, "_spin_grid", Mock(return_value=grid))
        monkeypatch.setattr(views, "render", lambda request, template, context: context)

        context = views.slot_bonus(request)
        return context["result"], player, game, session

    return play


@pytest.mark.parametrize(
    ("starting_spins", "scatter_positions", "remaining", "awarded"),
    [
        pytest.param(0, ((1, 1), (3, 2), (5, 3)), 10, 10, id="TC-22"),
        pytest.param(0, ((1, 1), (3, 2)), 0, 0, id="TC-23"),
        pytest.param(1, (), 0, 0, id="TC-24"),
        pytest.param(1, ((1, 1), (3, 2), (5, 3)), 0, 0, id="TC-25"),
    ],
)
def test_free_spin_rules(play_spin, starting_spins, scatter_positions, remaining, awarded):
    result, player, game, session = play_spin(make_grid(scatter_positions), starting_spins)

    is_free = starting_spins > 0
    views._spin_grid.assert_called_once_with(is_free=is_free)
    assert result["is_free"] is is_free
    assert result["free_spins_left"] == player.free_spins_bonus == remaining
    assert result["fs_awarded"] == awarded
    assert result["total_win"] == Decimal("0.00")
    views.apply_win.assert_not_called()

    if is_free:
        views.apply_bet.assert_not_called()
        views.Transaction.objects.create.assert_called_once_with(
            player=player,
            transaction_type=views.Transaction.TxType.BET,
            amount=Decimal("0"),
            game=game,
            session=session,
            meta={"free_spin": True, "nominal_bet": "5.00"},
        )
    else:
        views.Transaction.objects.create.assert_not_called()
        views.apply_bet.assert_called_once_with(
            player=player,
            game=game,
            amount=Decimal("5.00"),
            meta={"free_spin": False},
            session=session,
        )

    if is_free or awarded:
        player.save.assert_called_once_with(update_fields=["free_spins_bonus"])
    else:
        player.save.assert_not_called()


@pytest.mark.parametrize("expected_total", [pytest.param(Decimal("21.00"), id="TC-26")])
def test_sum_of_line_wins(play_spin, expected_total):
    grid = [["LOW1"] * 3 for _ in range(3)] + [["LOW2"] * 3 for _ in range(2)]
    result, player, game, session = play_spin(grid, free_spins=0)

    expected_lines = [
        {"line": number, "symbol": "LOW1", "count": 3, "win": "1.05"}
        for number in range(1, 21)
    ]
    assert result["total_win"] == expected_total
    assert result["line_wins"] == expected_lines
    views.apply_win.assert_called_once_with(
        player=player,
        game=game,
        amount=expected_total,
        meta={"lines": expected_lines},
        session=session,
    )
