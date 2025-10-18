#!/usr/bin/env python3
import argparse
import pandas as pd
from tqdm import tqdm
import pyshark

parser = argparse.ArgumentParser()
parser.add_argument('--pcap', required=True, help='Input pcap file')
parser.add_argument('--out', required=True, help='Output CSV file for flows')
parser.add_argument('--timeout', type=float, default=60.0, help='session timeout in seconds')
args = parser.parse_args()

cap = pyshark.FileCapture(args.pcap, keep_packets=False)
flows = {}

def key_from_pkt(pkt):
    try:
        ip = pkt.ip
        src = ip.src
        dst = ip.dst
        proto = pkt.transport_layer
        sport = pkt[pkt.transport_layer].srcport if hasattr(pkt[pkt.transport_layer],'srcport') else pkt[pkt.transport_layer].srcport
        dport = pkt[pkt.transport_layer].dstport if hasattr(pkt[pkt.transport_layer],'dstport') else pkt[pkt.transport_layer].dstport
        return (src,dst,sport,dport,proto)
    except Exception:
        return None

for pkt in tqdm(cap):
    k = key_from_pkt(pkt)
    if k is None:
        continue
    ts = float(pkt.sniff_timestamp)
    plen = int(pkt.length)
    if k not in flows:
        flows[k] = {'start': ts, 'end': ts, 'packets': 1, 'src_bytes': plen, 'dst_bytes': 0,
                    'src': k[0], 'dst': k[1], 'sport': k[2], 'dport': k[3], 'proto': k[4]}
    else:
        f = flows[k]
        f['end'] = ts
        f['packets'] += 1
        f['src_bytes'] += plen

rows = []
for k,f in flows.items():
    duration = f['end'] - f['start']
    bytes_per_sec = (f['src_bytes'] + f['dst_bytes']) / (duration + 1e-6)
    rows.append({
        'duration': duration,
        'packets': f['packets'],
        'src_bytes': f['src_bytes'],
        'dst_bytes': f['dst_bytes'],
        'bytes_per_sec': bytes_per_sec,
        'protocol': f['proto'],
        'flags_syn': 0, 'flags_ack': 0,
        'dst_port': int(f['dport']) if str(f['dport']).isdigit() else 0,
        'failed_logins': 0,
        'label': 'BENIGN'
    })

df = pd.DataFrame(rows)
df.to_csv(args.out, index=False)
print('Wrote flows to', args.out)
