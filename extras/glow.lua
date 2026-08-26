-- Sorbet Noir — mint bloom + groupbar tint.
--
-- Omarchy drops every *.lua from a theme installed via `omarchy theme install`,
-- because a theme's hyprland.lua runs code at login. The border gradient still
-- comes through (it lives in colors.toml as hyprland_active_border), but the
-- shadow and groupbar colors below do not. Append this to
-- ~/.config/hypr/looknfeel.lua to get them back.

hl.config({
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

  group = {
    groupbar = {
      text_color = "rgb(e9e9ef)",
      text_color_inactive = "rgba(e9e9ef90)",
      col = {
        active = "rgba(a8f0dc30)",
        inactive = "rgba(00000040)",
      },
    },
  },
})
