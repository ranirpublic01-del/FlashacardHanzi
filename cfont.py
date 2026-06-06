from fontTools.ttLib import TTFont

font_path = r"D:\gangjian-handwriting.ttf\gangjian-handwriting.ttf"
output_path = r"D:\gangjian-handwriting.ttf\gangjian-handwriting-renamed.ttf"

font = TTFont(font_path)

new_family = "Gangjian Handwriting"
new_full = "Gangjian Handwriting Regular"
new_postscript = "GangjianHandwriting-Regular"

for record in font["name"].names:
    if record.nameID == 1:  # Font Family
        record.string = new_family.encode("utf-16-be")

    elif record.nameID == 4:  # Full Font Name
        record.string = new_full.encode("utf-16-be")

    elif record.nameID == 6:  # PostScript Name
        record.string = new_postscript.encode("utf-16-be")

font.save(output_path)

print("Done!")
print("Saved to:", output_path)