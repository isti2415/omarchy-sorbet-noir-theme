-- Sorbet Noir look'n'feel — rounded & airy, subtle glass, smooth & flowy.
-- https://wiki.hypr.land/Configuring/Basics/Variables/

hl.config({
  general = {
    -- Rounded & airy: generous black gutters so the pastel borders breathe.
    gaps_in = 4,
    gaps_out = 6,
    border_size = 2,
  },

  decoration = {
    rounding = 10,

    -- Dim unfocused windows so the focused one's colors pop harder.
    dim_inactive = true,
    dim_strength = 0.18,
    dim_around = 0.1,

    -- Subtle glass: blur what sits behind translucent surfaces.
    blur = {
      enabled = true,
      size = 4,
      passes = 2,
      new_optimizations = true,
      ignore_opacity = true,
      popups = true,
      popups_ignorealpha = 0.2,
      -- Lift what sits behind translucent surfaces: on an all-black desktop
      -- a neutral blur just smears black into black. Brightening slightly
      -- keeps the backdrop readable as shapes without breaking the theme.
      brightness = 1.35,
      contrast = 1.15,
      noise = 0.015,
    },
  },

  -- The mint bloom itself is defined by the theme (themes/sorbet-noir/hyprland.lua)
  -- so it re-tints if you ever switch themes.
})

-- Subtle glass on the shell surfaces: bar, launcher, menus, notifications.
hl.layer_rule({ match = { namespace = "omarchy-bar" }, blur = true, ignore_alpha = 0.05 })
hl.layer_rule({
  match = { namespace = "^(omarchy-menu|omarchy-image-selector|omarchy-emojis|omarchy-clipboard|omarchy-keyboard-panel|omarchy-notifications|omarchy-osd)$" },
  blur = true,
  ignore_alpha = 0.05,
})

-- ── Smooth & flowy motion ────────────────────────────────────────────────
-- Longer, softer easing than stock. Higher speed numbers = longer duration.
hl.curve("softOut", { type = "bezier", points = { { 0.16, 1 }, { 0.3, 1 } } })
hl.curve("gentle", { type = "bezier", points = { { 0.34, 1.16 }, { 0.64, 1 } } })
hl.curve("silk", { type = "bezier", points = { { 0.45, 0 }, { 0.15, 1 } } })
hl.curve("linear", { type = "bezier", points = { { 0, 0 }, { 1, 1 } } })

hl.animation({ leaf = "global", enabled = true, speed = 10, bezier = "softOut" })

-- Slow border travel makes the pastel ribbon visibly sweep on focus change.
hl.animation({ leaf = "border", enabled = true, speed = 9, bezier = "softOut" })

hl.animation({ leaf = "windows", enabled = true, speed = 5.5, bezier = "softOut" })
hl.animation({ leaf = "windowsIn", enabled = true, speed = 6, bezier = "gentle", style = "popin 90%" })
hl.animation({ leaf = "windowsOut", enabled = true, speed = 4, bezier = "silk", style = "popin 92%" })

hl.animation({ leaf = "fade", enabled = true, speed = 4.5, bezier = "softOut" })
hl.animation({ leaf = "fadeIn", enabled = true, speed = 3, bezier = "softOut" })
hl.animation({ leaf = "fadeOut", enabled = true, speed = 2.5, bezier = "silk" })
hl.animation({ leaf = "fadeSwitch", enabled = false })

hl.animation({ leaf = "layers", enabled = true, speed = 5, bezier = "softOut" })
hl.animation({ leaf = "layersIn", enabled = true, speed = 5, bezier = "gentle", style = "fade" })
hl.animation({ leaf = "layersOut", enabled = true, speed = 3.5, bezier = "silk", style = "fade" })
hl.animation({ leaf = "fadeLayersIn", enabled = true, speed = 3, bezier = "softOut" })
hl.animation({ leaf = "fadeLayersOut", enabled = true, speed = 2.5, bezier = "silk" })

-- Workspaces glide instead of cutting (stock has this off).
hl.animation({ leaf = "workspaces", enabled = true, speed = 6, bezier = "softOut", style = "slidefade 15%" })
hl.animation({ leaf = "specialWorkspace", enabled = true, speed = 5, bezier = "gentle", style = "slidevert" })
