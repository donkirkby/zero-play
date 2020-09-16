from zero_play.rules_formatter import convert_markdown


def test_basic_markdown():
    markdown = """\
Hello, *World!*
"""
    expected_html = """\
<p>Hello, <em>World!</em></p>"""

    html = convert_markdown(markdown)

    assert html == expected_html


def test_title():
    markdown = """\
---
title: Greeting

---
Hello, *World!*
"""
    expected_html = """\
<h1>Greeting</h1>
<p>Hello, <em>World!</em></p>"""

    html = convert_markdown(markdown)

    assert html == expected_html
