import re

def parse_menu_lines(data):
    menu_list = []

    for section in data:
        for line in section:
            # Use regex to find lines ending with a price
            match = re.search(r'(\d+)$', line)
            if match:
                price = int(match.group(1))
                if price == 0:
                    price = None
                item = line[:match.start()].strip()
            else:
                price = None
                item = line.strip()
            menu_list.append({"item": item, "price": price})
    return menu_list
