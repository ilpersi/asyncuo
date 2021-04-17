import urllib.request
import xml.etree.ElementTree as ET

from misc.generate_packet_table import generate

req = urllib.request.Request(
    'https://ruosi.org/packetguide/index.xml',
    data=None,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/66.0.3359.139 Safari/537.36'
    }
)

with urllib.request.urlopen(req) as response:
    xml = response.read()

packet_table = {x: {'size': 0xFFFF, 'from': 'N/A', 'name': 'Unknown', 'desc': 'N/A'} for x in range(0xFF + 1)}

tree = ET.fromstring(xml)
for packet in tree.iter('Packet'):
    packet_id = (packet.attrib['id'])
    if '.' in packet_id:
        continue
    else:
        packet_id = int(packet_id, 16)

    packet_size = int(packet.attrib['size'])
    packet_from = packet.attrib['from']

    packet_name = packet.find('Name').text
    packet_desc = packet.find('Desc').text

    packet_table[packet_id]['size'] = packet_size if packet_size != -1 else 0
    packet_table[packet_id]['from'] = packet_from
    packet_table[packet_id]['name'] = packet_name
    packet_table[packet_id]['desc'] = packet_desc

generate(packet_table)
