"""One-off runner for Lab 4 Part 4 — prints console-style log; not required in submission zip."""
from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage

from agent import build_graph


def _tool_trace(messages: list[BaseMessage]) -> list[str]:
    names: list[str] = []
    for msg in messages:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            for tc in msg.tool_calls:
                if isinstance(tc, dict):
                    names.append(str(tc.get("name", "?")))
                else:
                    names.append(getattr(tc, "name", "?"))
    return names


def _final_reply(messages: list[BaseMessage]) -> str:
    last = messages[-1]
    if isinstance(last, AIMessage):
        return (last.content or "").strip() or "(no text; possibly tool-only turn)"
    return str(last)


def run_case(app, name: str, user_text: str) -> tuple[str, list[str], str]:
    out = io.StringIO()
    with redirect_stdout(out):
        print(f"\n{'=' * 60}")
        print(f"TEST: {name}")
        print(f"Ban: {user_text}")
        print("-" * 60)
        result = app.invoke({"messages": [HumanMessage(content=user_text)]})
        conv = result["messages"]
        tools = _tool_trace(conv)
        reply = _final_reply(conv)
        print(f"Tools invoked (order): {tools if tools else '(none)'}")
        print(f"TravelBuddy: {reply}")
        # Debug: tool returns (short)
        for msg in conv:
            if isinstance(msg, ToolMessage):
                content = (msg.content or "")[:500]
                print(f"  [Tool {msg.name}] {content}{'...' if len(msg.content or '') > 500 else ''}")
    return out.getvalue(), tools, reply


def _pass_fail(idx: int, tools: list[str], reply: str) -> str:
    r = reply.lower()
    if idx == 1:
        asks_more = any(
            k in r
            for k in ("sở thích", "so thich", "ngân sách", "ngan sach", "thời gian", "thoi gian")
        )
        return "Pass" if (not tools and asks_more) else "Fail (can chao hoi + hoi them so thich/ngan sach/thoi gian)"
    if idx == 2:
        if "search_flights" in tools and "search_hotels" not in tools and "calculate_budget" not in tools:
            return "Pass"
        return f"Fail (ky vong chi search_flights; nhan: {tools})"
    if idx == 3:
        need = {"search_flights", "search_hotels", "calculate_budget"}
        got = set(tools)
        return "Pass" if need <= got else f"Fail (thieu tool: {sorted(need - got)})"
    if idx == 4:
        asks_hotel_info = any(
            k in r for k in ("thành phố", "thanh pho", "bao nhiêu đêm", "bao nhieu dem", "ngân sách", "ngan sach")
        )
        return "Pass" if (not tools and asks_hotel_info) else "Fail (can hoi thanh pho/so dem/ngan sach truoc)"
    if idx == 5:
        hints = (
            "du lich",
            "du lịch",
            "pham vi",
            "phạm vi",
            "khong the",
            "không thể",
            "ve may bay",
            "vé máy bay",
            "travelbuddy",
            "ho tro",
            "hỗ trợ",
        )
        ok = (not tools) and any(h in r for h in hints)
        return "Pass" if ok else "Fail (can tu choi + gioi thieu pham vi du lich)"
    return "?"


def _markdown_report(
    cases: list[tuple[str, str]],
    rows: list[tuple[list[str], str, str]],
) -> str:
    def inp(i: int) -> str:
        return cases[i][1]

    lines = [
        "# Lab 4 Test Results - TravelBuddy",
        "",
        "Ket qua ghi tu `python run_lab4_tests.py` (Part 4 - kiem thu).",
        "",
        "## Test 1 - Direct Answer (No Tool)",
        f'- **Input**: "{inp(0)}"',
        "- **Expected**: Agent chao hoi, gioi thieu kha nang, khong goi tool.",
        f"- **Tools invoked**: `{rows[0][0]}`",
        f"- **Actual (TravelBuddy)**: {rows[0][1]}",
        f"- **Pass/Fail**: {rows[0][2]}",
        "",
        "## Test 2 - Single Tool Call",
        f'- **Input**: "{inp(1)}"',
        "- **Expected**: Agent goi `search_flights` va tra danh sach chuyen bay.",
        f"- **Tools invoked**: `{rows[1][0]}`",
        f"- **Actual (TravelBuddy)**: {rows[1][1]}",
        f"- **Pass/Fail**: {rows[1][2]}",
        "",
        "## Test 3 - Multi-Step Tool Chaining",
        f'- **Input**: "{inp(2)}"',
        "- **Expected**: Lien tiep `search_flights` -> `search_hotels` -> `calculate_budget`, sau do tong hop.",
        f"- **Tools invoked**: `{rows[2][0]}`",
        f"- **Actual (TravelBuddy)**: {rows[2][1]}",
        f"- **Pass/Fail**: {rows[2][2]}",
        "",
        "## Test 4 - Missing Info",
        f'- **Input**: "{inp(3)}"',
        "- **Expected**: Hoi lai thong tin thieu truoc khi goi tool.",
        f"- **Tools invoked**: `{rows[3][0]}`",
        f"- **Actual (TravelBuddy)**: {rows[3][1]}",
        f"- **Pass/Fail**: {rows[3][2]}",
        "",
        "## Test 5 - Guardrail / Refusal",
        f'- **Input**: "{inp(4)}"',
        "- **Expected**: Tu choi lich su, chuyen huong sang du lich.",
        f"- **Tools invoked**: `{rows[4][0]}`",
        f"- **Actual (TravelBuddy)**: {rows[4][1]}",
        f"- **Pass/Fail**: {rows[4][2]}",
        "",
        "## Tong ket",
    ]
    passed = sum(1 for r in rows if r[2].startswith("Pass"))
    lines.append(f"- So test dat: **{passed}/5**")
    lines.append("- Log console day du: xem file `test_console_log.txt` (cung thu muc).")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    app = build_graph()
    cases = [
        (
            "Test 1 - Direct Answer",
            "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.",
        ),
        (
            "Test 2 - Single Tool",
            "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng",
        ),
        (
            "Test 3 - Multi-Step Chain",
            "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!",
        ),
        ("Test 4 - Missing Info", "Tôi muốn đặt khách sạn"),
        ("Test 5 - Guardrail", "Giải giúp tôi bài tập lập trình Python về linked list"),
    ]
    full_log = io.StringIO()
    rows: list[tuple[list[str], str, str]] = []
    for i, (title, text) in enumerate(cases, start=1):
        block, tools, reply = run_case(app, title, text)
        full_log.write(block)
        print(block, end="")
        pf = _pass_fail(i, tools, reply)
        rows.append((tools, reply, pf))

    log_path = Path(__file__).resolve().parent / "test_console_log.txt"
    log_path.write_text(full_log.getvalue(), encoding="utf-8")
    md_path = Path(__file__).resolve().parent / "test_results.md"
    md_path.write_text(_markdown_report(cases, rows), encoding="utf-8")
    print(f"\nLog also saved to: {log_path}")
    print(f"Markdown report: {md_path}")


if __name__ == "__main__":
    main()
