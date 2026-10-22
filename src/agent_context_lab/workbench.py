"""Optional read-only Streamlit interface over immutable Run Bundles.

Start with: uv run --extra workbench streamlit run src/agent_context_lab/workbench.py
"""

from pathlib import Path
import json
import streamlit as st
import plotly.express as px

from agent_context_lab.storage import load_bundle

st.set_page_config(page_title="Agent Context Lab", layout="wide")
st.title("Agent Context Lab · Research Workbench")
st.caption("Phase 1: read-only inspection of local scripted experiments")
root = Path(st.sidebar.text_input("Run directory", "runs"))
paths = sorted(root.glob("*/*/*/manifest.json"))
if not paths:
    st.info("No runs found. Execute `uv run acl demo` first.")
    st.stop()
options = {str(p.parent.relative_to(root)): p.parent for p in paths}
selection = st.selectbox("Run attempt", options=list(options))
record = load_bundle(options[selection])
manifest = record["manifest"]
result = record["result"]
metrics = st.columns(4)
metrics[0].metric("Status", result["status"] if result else "incomplete")
metrics[1].metric("Model calls", len(record["model_calls"]))
metrics[2].metric("Projections", len(record["projections"]))
metrics[3].metric("Events", len(record["events"]))
t1, t2, t3 = st.tabs(["Trajectory", "Context", "Evidence"])
with t1:
    st.dataframe([{"seq": e["sequence_number"], "event": e["event_type"],
                   "elapsed_ms": round(e["monotonic_offset_ns"] / 1e6, 2),
                   "payload": json.dumps(e["payload"], ensure_ascii=False)}
                  for e in record["events"]], use_container_width=True)
    if record["projections"]:
        st.plotly_chart(px.line([{"call": p["call_id"], "estimated_input_tokens":
                                  p["estimated_input_tokens"]} for p in record["projections"]],
                                x="call", y="estimated_input_tokens", markers=True),
                        use_container_width=True)
with t2:
    ids = [p["call_id"] for p in record["projections"]]
    call = st.selectbox("Model call", ids)
    projection = next(p for p in record["projections"] if p["call_id"] == call)
    st.caption("Token values are estimates, not provider-reported usage")
    st.json({k: v for k, v in projection.items() if k != "ordered_messages"})
    st.dataframe(projection["ordered_messages"], use_container_width=True)
with t3:
    st.subheader("Manifest")
    st.json(manifest)
    st.subheader("Result")
    st.json(result)
    st.download_button("Export run summary (JSON)",
                       json.dumps({"manifest": manifest, "result": result},
                                  ensure_ascii=False, indent=2),
                       file_name="run_summary.json", mime="application/json")
