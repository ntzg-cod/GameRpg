"""End-to-end tests for the BattleEngine using only fakes (SRP/DIP/LSP).

The engine never calls input/print/time directly, so these tests run
headless and instantly while asserting the exact turn order.
"""

from __future__ import annotations

import random

from battle.actions import ATTACK, build_registry
from battle.clock import FakeClock
from battle.engine import BattleEngine
from battle.strategies import RandomDecisionStrategy

from conftest import (
    ACTIONS_WITH_FLEE,
    FakeCombatant,
    QueueStrategy,
    RecordingView,
    ScriptedController,
)


def make_engine(controller, strategy, actions=None, view=None, clock=None):
    return BattleEngine(
        view=view or RecordingView(),
        player_controller=controller,
        enemy_strategy=strategy,
        actions=actions,
        clock=clock or FakeClock(),
    )


class AlwaysAttack:
    """DecisionStrategy that always chooses 'a' (unbounded rounds)."""

    def decide(self, context):
        return "a"


def test_player_kills_enemy_before_it_acts():
    """Player attacks first and kills a weak enemy; enemy never acts."""
    player = FakeCombatant("Hero", hp=100)
    enemy = FakeCombatant("Foe", hp=5)
    engine = make_engine(ScriptedController("a"), QueueStrategy("d"))
    engine.run(player, enemy)

    assert enemy.hp == 0
    assert player.log == ["Hero->attack:10"]
    assert enemy.log == []  # Foe died before its turn


def test_enemy_acts_when_surviving_player_attack():
    """With a tougher enemy, the fight lasts 3 rounds with correct order."""
    player = FakeCombatant("Hero", hp=100)
    enemy = FakeCombatant("Foe", hp=25)  # dies on the 3rd hero attack
    engine = make_engine(
        ScriptedController("a", "a", "a"),
        QueueStrategy("a", "a", "a"),
    )
    engine.run(player, enemy)

    # Rounds 1 & 2: Hero a, Foe a. Round 3: decide() runs, Hero a kills ->
    # Foe never applies its action (decide is per-round, action is not).
    assert player.log == ["Hero->attack:10", "Hero->attack:10", "Hero->attack:10"]
    assert enemy.log == ["Foe->attack:10", "Foe->attack:10"]


def test_view_receives_status_and_defeat_events():
    view = RecordingView()
    player = FakeCombatant("Hero", hp=100)
    enemy = FakeCombatant("Foe", hp=5)
    engine = make_engine(ScriptedController("a"), QueueStrategy("a"), view=view)
    engine.run(player, enemy)

    assert view.status == [("Hero", "Foe")]
    assert view.defeats == ["Foe"]
    assert view.separators == 0  # fight ended before any separator


def test_round_separator_and_clock_sleep_per_completed_round():
    view = RecordingView()
    clock = FakeClock()
    player = FakeCombatant("Hero", hp=100)
    enemy = FakeCombatant("Foe", hp=25)
    engine = make_engine(
        ScriptedController("a", "a", "a"),
        QueueStrategy("a", "a", "a"),
        view=view,
        clock=clock,
    )
    engine.run(player, enemy)

    # Rounds 1 & 2 complete (sleep+sep each); round 3 ends on the kill.
    assert clock.sleeps == [1, 1]
    assert view.separators == 2
    assert view.defeats == ["Foe"]


def test_engine_runs_with_reduced_action_set():
    """OCP: engine works with ANY registry, including a reduced one."""
    only_attack = build_registry((ATTACK,))
    player = FakeCombatant("Hero", hp=100)
    enemy = FakeCombatant("Foe", hp=5)
    engine = make_engine(
        ScriptedController("a"), QueueStrategy("a"), actions=only_attack
    )
    engine.run(player, enemy)
    assert enemy.hp == 0


def test_engine_accepts_flee_action_extension():
    """OCP: a brand-new action (r=run) works without modifying the engine."""
    player = FakeCombatant("Hero", hp=100)
    enemy = FakeCombatant("Foe", hp=5)
    engine = make_engine(
        ScriptedController("r", "a"),  # flee round 1, attack round 2
        QueueStrategy("a", "a"),  # decide() is called every round, incl. the last
        actions=ACTIONS_WITH_FLEE,
    )
    engine.run(player, enemy)

    # Fleeing deals no damage, so Foe survives round 1 and attacks once.
    # In round 2 Hero attacks and kills it (decide ran but action never applied).
    assert "Hero->flee" in player.log
    assert enemy.log == ["Foe->attack:10"]
    assert enemy.hp == 0  # killed by Hero's round-2 attack


def test_engine_works_with_non_character_combatant_lsp():
    """LSP: any object satisfying the Combatant protocol can battle."""
    player = FakeCombatant("P", hp=100)
    enemy = FakeCombatant("E", hp=25)
    engine = make_engine(
        ScriptedController("a", "a", "a"),
        RandomDecisionStrategy(rng=random.Random(1)),
    )
    engine.run(player, enemy)  # must not raise
    assert enemy.hp == 0 or player.hp < 100


def test_guard_does_not_linger_into_next_round():
    """Regression: a guard set last round is cleared by begin_turn().

    Foe defends every round. Hero defends round 1 (both guards cancel),
    then attacks round 2. Because begin_turn() clears Foe's stale guard,
    Hero's round-2 attack lands at FULL damage and kills Foe (10, not
    the blocked 5). Without the fix Foe would survive and the scripted
    queues would empty -> the test would crash.
    """
    player = FakeCombatant("Hero", hp=100)
    enemy = FakeCombatant("Foe", hp=10)  # dies to a single full hit
    view = RecordingView()

    class AlwaysDefend:
        def decide(self, context):
            return "d"

    engine = make_engine(
        ScriptedController("d", "a"),  # Hero defends r1, attacks r2
        AlwaysDefend(),
        view=view,
    )
    engine.run(player, enemy)

    assert enemy.hp == 0
    assert view.defeats == ["Foe"]


def test_guard_blocks_same_round_then_expires_next_round():
    """A guard protects during its own round, then expires next round."""
    player = FakeCombatant("Hero", hp=30)  # dies exactly after r1+r2
    enemy = FakeCombatant("Foe", hp=100, damage=20)
    view = RecordingView()

    engine = make_engine(
        ScriptedController("d", "a"),  # Hero defends r1 only
        AlwaysAttack(),
        view=view,
    )
    engine.run(player, enemy)

    # r1: guard blocks 20->10 (hero 20). r2: guard expired, full 20 -> hero 0.
    # If the guard lingered, r2 would be blocked and Hero would survive
    # (and the empty queue would crash). Dying in exactly round 2 proves expiry.
    assert view.defeats == ["Hero"]
    assert view.separators == 1  # only round 1 completed
