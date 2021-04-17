def generate(packet_table_info):
    print('packet_lengths = {')
    for packet_id, packet_info in packet_table_info.items():
        print("  0x{:02X}: 0x{:04X},  # {} FROM: {}"
              .format(packet_id, packet_info['size'], packet_info['name'], packet_info['from']))
    print('}')