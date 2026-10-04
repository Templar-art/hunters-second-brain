"""Bebita stock take (Hunter, 2026-10-04), transcribed from his notes.
Each product: line, role (top/bottom/one-piece/set/layer/accessory), and colour -> {size: qty}.
Run to print totals and write stock.csv.
"""
import csv, os

OS = "One size"
STOCK = [
 # ---- ACTIVE: bottoms
 ("Scrunch Shorts", "active", "bottom", {"Red":{"S":3,"M":2},"Light Blue":{"S":2,"M":1,"L":1},"Dark Blue":{"S":1,"M":4},
   "Highlighter Pink":{"S":2,"M":5},"Peach":{"M":1},"Black":{"S":1,"L":4},"Pink":{"S":1}}),
 ("Dynamic Seamless Shorts", "active", "bottom", {"Grey":{"XS":1},"Teal":{"S":1},"Blue":{"XS":1,"S":2,"M":2},"Pink":{"M":1},
   "Lilac":{"S":3},"Coral":{"XS":1,"S":2},"Baby Blue":{"XS":2,"S":1},"Baby Pink":{"L":1}}),
 ("V-Back Shorts", "active", "bottom", {"Blue":{"S":1,"M":2,"L":1},"Pink":{"XS":1,"L":1},"Black":{"XS":1,"M":1,"L":3},"Brown":{"M":3,"L":2}}),
 ("V-Back Leggings", "active", "bottom", {"Blue":{"S":4,"M":4},"Brown":{"M":2,"L":2},"Pink":{"S":1,"L":1},
   "Black":{"XS":1,"M":2,"L":1},"Highlighter Pink":{"M":2,"L":1}}),
 ("Scrunch Pants", "active", "bottom", {"Pink":{"S":3,"M":1},"Navy":{"S":1},"Brown":{"S":1}}),
 ("Dynamic Leggings", "active", "bottom", {"Blue":{"S":3},"Bone Grey":{"XS":1}}),
 ("Dynamic Flares", "active", "bottom", {"Lilac":{"S":2,"M":2},"Black":{"S":1},"Blue":{"S":2,"M":1}}),
 # ---- ACTIVE: tops
 ("Cross Back Top", "active", "top", {"Lilac":{"S":3,"M":1},"Blue":{"S":2,"L":1},"Black":{"S":5,"M":1}}),
 ("Open Back Top", "active", "top", {"Blue":{"XS":1},"Pink":{"XS":1},"Brown":{"XS":1},"Black":{"XS":1}}),
 ("Cross Back Straight Top", "active", "top", {"Brown":{"XS":3,"S":2,"M":2,"L":1},"Blue":{"XS":3,"S":4,"M":3,"L":1},
   "Highlighter Pink":{"XS":2,"S":2,"M":3,"L":2},"Black":{"XS":1,"S":1,"M":1,"L":1}}),
 ("Halter Top", "active", "top", {"Teal":{"S":1},"Blue":{"S":1}}),
 ("Triangle Top", "active", "top", {"Blue":{"S":1},"Bone Grey":{"S":1},"Grey":{"S":1}}),
 ("Halter Neck Triangle Top", "active", "top", {"Blue":{"S":1,"M":2}}),
 ("Dynamic Top", "active", "top", {"Blush Pink":{"XS":2},"Baby Blue":{"XS":1,"L":1},"Lilac":{"XS":1,"S":2},"Coral":{"XS":2,"S":1,"L":1}}),
 ("Scrunch Halter Top", "active", "top", {"Lilac":{"S":1}}),
 ("Cross Back Twist Triangle Top", "active", "top", {"Red":{"S":1,"M":2,"L":2},"Highlighter Pink":{"S":1,"M":3},"Teal":{"S":1},
   "Pink":{"S":1,"M":1,"L":1},"Black":{"S":2,"M":1,"L":1},"Blue":{"S":2,"M":2,"L":1}}),
 ("Cross Back Thin Strap Triangle Top", "active", "top", {"Highlighter Pink":{"S":1}}),
 ("Two Tone Halter Top", "active", "top", {"Pink/White":{"S":1},"Black/White":{"S":1},"Brown/White":{"S":1},"Navy/White":{"S":1}}),
 ("2-in-1 Layered Long Sleeve Crop Top", "active", "top", {"Brown/White":{"S":3,"M":1},"Navy/White":{"M":1},"Black/White":{"M":1}}),
 # ---- ACTIVE: layers, sets, one-pieces
 ("Cropped Zip Jacket", "active", "layer", {"Lilac":{"M":2},"Black":{"S":1,"M":1,"L":1},"Blue":{"M":2},"Yellow":{"M":1}}),
 ("Cross Back Flare Set", "active", "set", {"Yellow":{"S":1}}),
 ("One Piece Short", "active", "one-piece", {"Blue":{"S":1,"M":3},"Red":{"S":1},"Pink":{"S":1},"Black":{"S":1}}),
 ("One Piece Long", "active", "one-piece", {"Blue":{"S":3},"Red":{"M":2},"Pink":{"M":1},"Black":{"M":1}}),
 # ---- SWIM
 ("Triangle Bikini Top", "swim", "top", {"White":{"XS":1},"Hot Pink":{"S":1},"Black":{"S":1,"M":1},"Brown":{"S":1},
   "Teal":{"XS":2,"M":1},"Blue":{"XS":1},"Coral":{"XS":1}}),
 ("Brazilian Bikini Set", "swim", "set", {"White":{"XS":6,"S":1,"M":2,"L":2},"Coral":{"XS":2,"S":2,"M":1,"XL":4},"Blue":{"XS":1,"L":2,"XL":2},
   "Red":{"L":2,"XL":2},"Black":{"L":3,"XL":2},"Teal":{"L":2,"XL":2},"Hot Pink":{"L":1,"XL":4},"Brown":{"L":1,"XL":2},
   "Purple/Teal":{"XL":1}}),
 ("V-Front Cheeky One Piece", "swim", "one-piece", {"Teal":{"XS":1,"S":2,"M":1,"XL":1},"Hot Pink":{"S":1,"L":2,"XL":1},"Black":{"L":1,"XL":1}}),
 ("Bikini Skirt", "swim", "bottom", {"Teal":{"XS-S":2,"M-L":1},"Hot Pink":{"M-L":1},"Black":{"M-L":1}}),
 ("Sarong", "swim", "accessory", {c:{OS:q} for c,q in [("Red",5),("Black",5),("Blue",5),("White",5),("Coral",5),("Hot Pink",3),("Teal",6),("Brown",5)]}),
 ("Bedazzled Cover Up", "swim", "accessory", {"Pink":{OS:1}}),
]

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    rows, tot = [], {"active":0,"swim":0}
    with open(os.path.join(here, "stock.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["Line","Product","Type","Colour","Size","Qty","Price (AUD)","Was price"])
        for name, line, role, cols in STOCK:
            n = sum(sum(s.values()) for s in cols.values()); tot[line] += n
            print(f"{line:6} {role:9} {name:36} {len(cols):2} colours {n:3} pcs")
            for c, sizes in cols.items():
                for s, q in sizes.items():
                    w.writerow([line.title(), name, role, c, s, q, "", ""])
    print("TOTAL", tot, sum(tot.values()), "pieces;", len(STOCK), "products")
