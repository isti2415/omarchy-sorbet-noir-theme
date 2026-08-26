-- Sorbet Noir — Hyprland color layer.
-- Four-stop pastel ribbon on the focused window, plus a mint AMOLED bloom.

local active_border_color = {
  colors = {
    "rgba(a8f0dcff)", -- mint
    "rgba(a2c4ffff)", -- sky
    "rgba(dcaaffff)", -- lilac
    "rgba(ff9aa9ff)", -- rose
  },
  angle = 45,
}

local inactive_border_color = "rgba(20202aaa)"

hl.config({
  general = {
    col = {
      active_border = active_border_color,
      inactive_border = inactive_border_color,
    },
  },

  group = {
    col = {
      border_active = active_border_color,
      border_inactive = inactive_border_color,
    },

    groupbar = {
      text_color = "rgb(e9e9ef)",
      text_color_inactive = "rgba(e9e9ef90)",
      col = {
        active = "rgba(a8f0dc30)",
        inactive = "rgba(00000040)",
      },
    },
  },

  decoration = {
    -- Mint glow: only the focused window blooms, so it floats off the black.
    shadow = {
      enabled = true,
      range = 18,
      render_power = 3,
      color = "rgba(a8f0dc20)",
      color_inactive = "rgba(00000000)",
    },
  },
})
