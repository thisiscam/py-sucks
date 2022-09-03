from xml.etree import ElementTree

from sucks import *


def test_custom_command():
    # Ensure a custom-built command generates the expected XML payload
    c = VacBotCommand("CustomCommand", {"type": "customtype"})
    assert (
        ElementTree.tostring(c.to_xml())
        == b'<ctl td="CustomCommand" type="customtype" />'
    )


def test_custom_command_inner_tag():
    # Ensure a custom-built command generates the expected XML payload
    c = VacBotCommand("CustomCommand", {"customtag": {"customvar": "customvalue"}})
    assert (
        ElementTree.tostring(c.to_xml())
        == b'<ctl td="CustomCommand"><customtag customvar="customvalue" /></ctl>'
    )


def test_custom_command_noargs():
    # Ensure a custom-built command with no args generates XML without an args element
    c = VacBotCommand("CustomCommand")
    assert ElementTree.tostring(c.to_xml()) == b'<ctl td="CustomCommand" />'


def test_clean_command():
    c = Clean()
    assert (
        ElementTree.tostring(c.to_xml())
        == b'<ctl td="Clean"><clean type="auto" speed="standard" /></ctl>'
    )  # protocol has attribs in other order
    c = Clean("edge", "high")
    assert (
        ElementTree.tostring(c.to_xml())
        == b'<ctl td="Clean"><clean type="border" speed="strong" /></ctl>'
    )  # protocol has attribs in other order


def test_edge_command():
    c = Edge()
    assert (
        ElementTree.tostring(c.to_xml())
        == b'<ctl td="Clean"><clean type="border" speed="strong" /></ctl>'
    )  # protocol has attribs in other order


def test_spot_command():
    c = Spot()
    assert (
        ElementTree.tostring(c.to_xml())
        == b'<ctl td="Clean"><clean type="spot" speed="strong" /></ctl>'
    )  # protocol has attribs in other order


def test_charge_command():
    c = Charge()
    assert (
        ElementTree.tostring(c.to_xml())
        == b'<ctl td="Charge"><charge type="go" /></ctl>'
    )


def test_stop_command():
    c = Stop()
    assert (
        ElementTree.tostring(c.to_xml())
        == b'<ctl td="Clean"><clean type="stop" speed="standard" /></ctl>'
    )


def test_play_sound_command():
    c = PlaySound()
    assert ElementTree.tostring(c.to_xml()) == b'<ctl td="PlaySound" sid="0" />'


def test_play_sound_command_with_sid():
    c = PlaySound(sid="1")
    assert ElementTree.tostring(c.to_xml()) == b'<ctl td="PlaySound" sid="1" />'


def test_get_clean_state_command():
    c = GetCleanState()
    assert ElementTree.tostring(c.to_xml()) == b'<ctl td="GetCleanState" />'


def test_get_charge_state_command():
    c = GetChargeState()
    assert ElementTree.tostring(c.to_xml()) == b'<ctl td="GetChargeState" />'


def test_get_battery_state_command():
    c = GetBatteryState()
    assert ElementTree.tostring(c.to_xml()) == b'<ctl td="GetBatteryInfo" />'


def test_move_command():
    c = Move(action="left")
    assert (
        ElementTree.tostring(c.to_xml())
        == b'<ctl td="Move"><move action="SpinLeft" /></ctl>'
    )

    c = Move(action="right")
    assert (
        ElementTree.tostring(c.to_xml())
        == b'<ctl td="Move"><move action="SpinRight" /></ctl>'
    )

    c = Move(action="turn_around")
    assert (
        ElementTree.tostring(c.to_xml())
        == b'<ctl td="Move"><move action="TurnAround" /></ctl>'
    )

    c = Move(action="forward")
    assert (
        ElementTree.tostring(c.to_xml())
        == b'<ctl td="Move"><move action="forward" /></ctl>'
    )

    c = Move(action="stop")
    assert (
        ElementTree.tostring(c.to_xml())
        == b'<ctl td="Move"><move action="stop" /></ctl>'
    )


def test_get_lifepsan_command():
    c = GetLifeSpan("main_brush")
    assert ElementTree.tostring(c.to_xml()) == b'<ctl td="GetLifeSpan" type="Brush" />'

    c = GetLifeSpan("side_brush")
    assert (
        ElementTree.tostring(c.to_xml()) == b'<ctl td="GetLifeSpan" type="SideBrush" />'
    )

    c = GetLifeSpan("filter")
    assert (
        ElementTree.tostring(c.to_xml())
        == b'<ctl td="GetLifeSpan" type="DustCaseHeap" />'
    )
