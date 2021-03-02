import pandas as pd
import xml.etree.cElementTree as ET

xs_base = r"{http://www.w3.org/2001/XMLSchema}"


def xsd_to_excel(filename, excel_name):
    tree = ET.ElementTree(file=filename)
    root = tree.getroot()

    res = []
    for child in root:
        tag = child.tag[len(xs_base):]
        name = "No name",
        desc = "No comments"
        restr = ""
        if tag in ["simpleType", "complexType"]:
            if "name" in child.attrib:
                name = child.attrib["name"]
                docs = list(child)[0]
                if docs.tag[len(xs_base):] == "annotation":
                    desc = docs[0].text

                restrictions = list(child.iter(xs_base +"restriction"))
                if restrictions:
                    restr += "Основа: " + restrictions[0].attrib["base"]
                    for r in restrictions[0]:
                        restr += "\n" + r.tag[len(xs_base):] + "=\"" + r.attrib["value"] + "\""
            else:
                print("Обнаружен элемент без имени")

            res.append({
                "Простота": tag,
                "Название": name,
                "Описание": desc,
                "ФЛК": restr,
            })
    df = pd.DataFrame(res)
    df.to_excel(excel_name)

if __name__ == "__main__":
    xsd_to_excel("gismu-types.xsd", "gismu-types.xlsx")
