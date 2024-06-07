import re

def find_price(data):
    menu_list = []
    for section in data:
        try:
            for line in section:
                try:
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
                except:
                    if line is None:
                        continue
                    menu_list.append({'item': line, "price": None})
        except:
            continue

    menu_list = [entry for entry in menu_list if entry['item']]
    return menu_list
