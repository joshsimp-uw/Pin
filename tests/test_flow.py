from app.flows.engine import registry, next_missing_field


def test_vpn_flow_missing_fields():
    flow = registry.get("vpn")
    collected = {"os": "Windows"}
    missing = next_missing_field(flow, collected)
    assert missing in flow.required_fields
