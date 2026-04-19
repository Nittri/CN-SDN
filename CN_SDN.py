from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

packet_count = {}

def _handle_PacketIn(event):
    packet = event.parsed
    if not packet:
        return

    src = packet.src

    if src not in packet_count:
        packet_count[src] = 0

    packet_count[src] += 1
    log.info(f"{src} count: {packet_count[src]}")

    # BLOCK
    if packet_count[src] > 20:
        log.info(f"Blocking for suspicious activity {src}")

        msg = of.ofp_flow_mod()
        msg.match.dl_src = src
        msg.actions = []  # DROP
        event.connection.send(msg)
        return

    # NORMAL FORWARDING
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    event.connection.send(msg)


def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)

