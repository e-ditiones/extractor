from lxml import etree as ET
from .count_illustration import count_illu


def extraction_image(doc_final, titre, editeur_scientifique, id_facsimile, ark):
    """
    Creates a TEI file with a list of all illustrations in a book according to
    information in facsimile tag in another TEI file.
    :param doc_final: str
        Path to file where to extract illustrations' information
    :param titre: str
        Title of the book
    :param id_facsimile: str
        Id of the book
    :param ark: str
        ark of the book
    """
    dossier_resultat_transformation = "./" + id_facsimile + "/xml/TEI/"
    document_final = ET.parse(doc_final)
    racine = document_final.getroot()
    # <grpList>
    root = ET.Element('TEI')
    root.set('id', id_facsimile)
    teiHeader = ET.SubElement(root, "teiHeader")
    fileDesc = ET.SubElement(teiHeader, "fileDesc")
    titleStmt = ET.SubElement(fileDesc, "titleStmt")
    title = ET.SubElement(titleStmt, "title")
    title.text = titre
    publicationStmt = ET.SubElement(fileDesc, "publicationStmt")
    publisher = ET.SubElement(publicationStmt, "publisher")
    publisher.text = editeur_scientifique
    sourceDesc = ET.SubElement(fileDesc, "sourceDesc")
    p = ET.SubElement(sourceDesc, "p")
    p.text = "Gallica"
    facsimile = ET.SubElement(root, "facsimile")
    facsimile.attrib["corresp"] = "#" + racine[1].attrib['{http://www.w3.org/XML/1998/namespace}id']
    facsimile.attrib["source"] = racine[1].attrib["source"]
     # on veut récupérer Decoration (BT4) et DropCapital (BT5)
      # parser le fichier dans l'output
      # aller dans TEI/facsimile
      # boucle for : pour chaque surface
    for surfaceGrp in racine[1]:
      # <listGrp>
        surfacegrp = ET.SubElement(facsimile, "surfaceGrp")
        surfacegrp.attrib["corresp"] = "#" + surfaceGrp.attrib['{http://www.w3.org/XML/1998/namespace}id']
        surfacegrp.attrib["type"] = surfaceGrp.attrib['type']
        for surface in surfaceGrp:
            if surface.attrib['corresp'] == "#BT4":
       # <list type="Decoration">
                surfaceimg = ET.SubElement(surfacegrp, "surface")
                surfaceimg.set("type", "decoration")
                surfaceimg.set("corresp", "#" + surface.attrib['{http://www.w3.org/XML/1998/namespace}id'])
                surfaceimg.set("facs", surface.attrib['source'])
            elif surface.attrib['corresp'] == "#BT5":
       # <list type="DropCapital">
                surfaceimg = ET.SubElement(surfacegrp, "surface")
                surfaceimg.set("type", "dropcapital")
                surfaceimg.set("corresp", "#" + surface.attrib['{http://www.w3.org/XML/1998/namespace}id'])
                surfaceimg.set("facs", surface.attrib['source'])
            elif surface.attrib['corresp'] == "BT6":
        # <list type="Figure">
                surfaceimg = ET.SubElement(surfacegrp, "surface")
                surfaceimg.set("type", "figure")
                surfaceimg.set("corresp", "#" + surface.attrib['{http://www.w3.org/XML/1998/namespace}id'])
                surfaceimg.set("facs", surface.attrib['source'])

    text = ET.SubElement(root, "text")
    body = ET.SubElement(text, "body")
    ET.SubElement(body, "p")
    with open(dossier_resultat_transformation + 'extration_img.xml', 'wb') as f:
        f.write(ET.tostring(root, encoding='utf-8'))

    count_illu(dossier_resultat_transformation + 'extration_img.xml')

    file = ET.parse(dossier_resultat_transformation + 'extration_img.xml')
    root = file.getroot()
    strings = ET.tostring(root, encoding='unicode')
    strings = strings.split("\n")
    final = ""
    for i in strings:
        if 'type="page"/>' in i:
            pass
        else:
            final += i
    with open(dossier_resultat_transformation + id_facsimile + "_" + ark + '_decoration.xml', 'wb') as f:
        f.write(bytes(final, encoding="utf-8"))
