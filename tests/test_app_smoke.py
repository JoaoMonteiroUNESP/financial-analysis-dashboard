from streamlit.testing.v1 import AppTest


def test_all_streamlit_pages_render_without_exceptions() -> None:
    app = AppTest.from_file("app.py").run(timeout=30)
    pages = app.sidebar.radio[0].options

    for page in pages:
        app.sidebar.radio[0].set_value(page).run(timeout=30)
        assert not app.exception, f"Streamlit page failed: {page}"


def test_dark_theme_and_million_unit_render() -> None:
    app = AppTest.from_file("app.py").run(timeout=30)
    app.sidebar.radio[1].set_value("R$ milhões")
    app.sidebar.radio[2].set_value("Escuro")
    app.run(timeout=30)

    assert not app.exception
    assert len(app.get("plotly_chart")) >= 2
