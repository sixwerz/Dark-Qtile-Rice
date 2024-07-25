from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook
from pathlib import Path
import os
import subprocess

mod = "mod4"
terminal = guess_terminal()

# --------------------------------------------------------
# Bars
# --------------------------------------------------------

# wm_bar = "polybar"
wm_bar = "qtile"

# --------------------------------------------------------
# Keys
# --------------------------------------------------------

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn('alacritty'), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),


    Key([mod], "c", lazy.spawn('firefox'), desc="browser"),
    Key([mod], "space",  lazy.widget["keyboardlayout"].next_keyboard()),
    Key([mod], "d", lazy.spawn('rofi -show drun'), desc="browser"),
    Key([mod, "shift"], "s", lazy.spawn('flameshot gui'), desc="ScreenShot"),
    Key([mod], "e", lazy.spawn('thunar'), desc="File manager"),
    
]

# --------------------------------------------------------
# Switch to Wayland
# --------------------------------------------------------

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


# --------------------------------------------------------
# Groups
# --------------------------------------------------------

groups = [
    Group("1", layout='monadtall'),
    Group("2", layout='monadtall'),
    Group("3", layout='monadtall'),
    Group("4", layout='monadtall'),
    Group("5", layout='monadtall'),
]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

# --------------------------------------------------------
# Layouts
# --------------------------------------------------------

layouts = [
    layout.Bsp(border_focus = "#f9f9f9", border_normal = '#000000', border_width=2, margin = 5), #EEB9FF
]

# --------------------------------------------------------
# Widgets
# --------------------------------------------------------

widget_list = [
                widget.TextBox(
                    text='Apps',
                    desc='',
                    padding=10,
                    mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("rofi -show drun")},
                    
                ),

                widget.WindowName(max_chars=30),

                widget.GroupBox(
                    padding_x = 5,
                    padding_y = 5,
                    rounded = False,
                    active = "#656565",
                    inactive = "#2b2b2b",
                    foreground = "#474c51",
                    highlight_method= "block",
                    this_current_screen_border = "#a4a4a4",
                    
                ),

                widget.Spacer(),

                widget.Systray(padding=5),
                
                widget.Battery(
                    format='{percent:2.0%}',
                    padding=5,
                ),
                
                widget.KeyboardLayout(configured_keyboards=['us','ru']),

                widget.Clock(
                    format="%Y-%m-%d %a | %I:%M %p",
                ),

]


# --------------------------------------------------------
# Vidget settings
# --------------------------------------------------------

widget_defaults = dict(
    font="JetBrainsMono",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

# ----------------------------------------------------
# Screens
# ----------------------------------------------------

if(wm_bar == "polybar"):
    screens = [Screen(top=bar.Gap(size=28))]

else:
    screens = [
        Screen(
            top=bar.Bar(
                widget_list,
                24,
                opacity=0.6,
                # font="JetBrainsMono",
                # background="#FFFFFF",
                # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
                # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            ),
        ),
    ]

# --------------------------------------------------------
# Drag floating layouts
# --------------------------------------------------------
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

# --------------------------------------------------------
# Other settings
# --------------------------------------------------------

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# --------------------------------------------------------
# Hooks
# --------------------------------------------------------

# HOOK startup
@hook.subscribe.startup_once
def autostart():
    autostartscript = "~/.config/qtile/autostart.sh"
    home = os.path.expanduser(autostartscript)
    subprocess.Popen([home])
