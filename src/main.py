import re
import requests

# Update this list
UNLOCKED_ITEM_LIST = [
    "1-25",
    "57-58",
    "61",
    "72",
    "76-77",
    "81",
    "83",
    "85-88",
    "90-94",
    "97",
    "119",
    "246",
]

ANY2_CARDS_URL = "https://raw.githubusercontent.com/any2cards/"
REMOTE_FILE_URL = ANY2_CARDS_URL + "frosthaven/master/data/items.js"


class Item:
    def __init__(self, item_id, points, expansion, image, xws):
        self.item_id = item_id
        self.points = points
        self.expansion = expansion
        self.image = image
        self.xws = xws

    def __repr__(self):
        return f"Item(name={self.item_id}, points={self.points}, expansion={self.expansion}, image={self.image}, xws={self.xws})"


class ItemsLoader:
    def __init__(self):
        self.items = self.load_items()
        self.valid_numbers = self.parse_number_list(UNLOCKED_ITEM_LIST)

    def parse_number_list(self, number_list):
        valid_numbers = set()
        for part in number_list:
            part = part.strip()
            if "-" in part:
                start, end = map(int, part.split("-"))
                valid_numbers.update(range(start, end + 1))
            else:
                valid_numbers.add(int(part))
        return valid_numbers

    def normalize_name(self, name):
        # Remove non-alphanumeric characters and leading zeros
        normalized_name = re.sub(r"\W+", "", name).lstrip("0").lower()
        # Ensure the name contains a number
        if not re.search(r"\d", normalized_name):
            return None
        return int(normalized_name.strip("item"))

    def load_items(self):
        response = requests.get(REMOTE_FILE_URL)
        response.raise_for_status()

        data = response.json()

        item_names = set()
        items = []
        for item in data:
            normalized_name = self.normalize_name(item["name"])
            if normalized_name and normalized_name not in item_names:
                item_names.add(normalized_name)
                items.append(
                    Item(
                        item_id=normalized_name,
                        points=item["points"],
                        expansion=item["expansion"],
                        image=item["image"],
                        xws=item["xws"],
                    )
                )
        return items

    def print_items(self):
        for item in self.items:
            print(item)

    def generate_html(self, output_filepath="../index.html"):
        html_content = """
        <html>
        <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                color: #333;
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                padding: 20px;
            }
            .title {
                width: 100%;
                text-align: center;
                margin-bottom: 20px;
            }
            .item {
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin: 10px;
                padding: 10px;
                text-align: center;
                width: 200px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .item img {
                max-width: 100%;
                border-radius: 5px;
            }
            .item p {
                font-size: 16px;
                font-weight: bold;
                margin: 10px 0 0;
            }
        </style>
        </head>
        <body>
        <div class="title">
            <h1>Current Unlocked Items</h1>
        </div>
        """
        for item in self.items:
            if item.item_id in self.valid_numbers:
                html_content += f'<div class="item"><img src="https://raw.githubusercontent.com/any2cards/frosthaven/master/images/{item.image}" alt="{item.item_id}"><p>{item.item_id}</p></div>\n'

        html_content += """
        <div class="item"><img src="https://raw.githubusercontent.com/any2cards/gloomhaven/master/images/items/gloomhaven/1-14/gh-010-war-hammer.png" alt="GH-10"><p>GH-10</p></div>\n
        <div class="item"><img src="https://raw.githubusercontent.com/any2cards/gloomhaven/master/images/items/gloomhaven/22-28/gh-025-jagged-sword.png" alt="GH-25"><p>GH-25</p></div>\n
        <div class="item"><img src="https://raw.githubusercontent.com/any2cards/gloomhaven/master/images/items/gloomhaven/64-151/gh-072b-shoes-of-happiness.png" alt="GH-72"><p>GH-72</p></div>\n
        <div class="item"><img src="https://raw.githubusercontent.com/any2cards/gloomhaven/master/images/items/gloomhaven/64-151/gh-105-flea-bitten-shawl.png" alt="GH-105"><p>GH-105</p></div>\n
        <div class="item"><img src="https://raw.githubusercontent.com/any2cards/gloomhaven/master/images/items/gloomhaven/64-151/gh-109-thiefs-hood.png" alt="GH-109"><p>GH-109</p></div>\n        <div class="item"><img src="https://raw.githubusercontent.com/any2cards/gloomhaven/master/images/items/gloomhaven/64-151/gh-116-fueled-falchion.png" alt="GH-116"><p>GH-116</p></div>\n
        </body>
        </html>
        """

        with open(output_filepath, "w") as file:
            file.write(html_content)

        print(f"HTML page generated at {output_filepath}")


def main():
    loader = ItemsLoader()
    # loader.print_items()
    loader.generate_html()


if __name__ == "__main__":
    main()
