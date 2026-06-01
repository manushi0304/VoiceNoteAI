import streamlit as st


def metric_card(title: str, value, emoji: str = ""):
    """Formal dark metric card with hover accent glow."""
    icon_html = f'<span style="font-size:1.1rem;opacity:0.7;margin-right:0.4rem;">{emoji}</span>' if emoji else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <h4>{icon_html}{title}</h4>
            <h2>{value}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(text: str, variant: str = "default"):
    """
    Minimal status badge. variant: 'success' | 'warning' | 'danger' | 'default'
    """
    colors = {
        "success": ("rgba(45,212,160,0.12)", "#2dd4a0", "rgba(45,212,160,0.25)"),
        "warning": ("rgba(240,180,41,0.12)", "#f0b429", "rgba(240,180,41,0.25)"),
        "danger":  ("rgba(245,101,101,0.10)", "#f56565", "rgba(245,101,101,0.25)"),
        "default": ("rgba(255,255,255,0.05)", "#64748b", "rgba(255,255,255,0.10)"),
    }
    bg, color, border = colors.get(variant, colors["default"])
    st.markdown(
        f"""
        <span style="
            display:inline-flex;align-items:center;
            background:{bg};color:{color};
            border:1px solid {border};
            padding:0.2rem 0.55rem;
            border-radius:4px;
            font-size:0.7rem;font-weight:600;
            letter-spacing:0.06em;text-transform:uppercase;
        ">{text}</span>
        """,
        unsafe_allow_html=True,
    )


def divider_label(text: str):
    """A subtle labelled divider for section separation."""
    st.markdown(
        f"""
        <div style="
            display:flex;align-items:center;gap:0.75rem;
            margin:1.25rem 0 1rem;
        ">
            <div style="flex:1;height:1px;background:rgba(255,255,255,0.07);"></div>
            <span style="
                font-size:0.68rem;font-weight:700;
                text-transform:uppercase;letter-spacing:0.12em;
                color:#3d4e68;white-space:nowrap;
            ">{text}</span>
            <div style="flex:1;height:1px;background:rgba(255,255,255,0.07);"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )