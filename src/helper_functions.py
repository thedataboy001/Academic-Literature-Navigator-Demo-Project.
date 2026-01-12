
from lxml import etree

def tei_to_text(tei_xml: str) -> str:
    root = etree.XML(tei_xml.encode("utf-8"))

    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    sections = []

    # Title
    title = root.xpath("//tei:titleStmt/tei:title/text()", namespaces=ns)
    if title:
        sections.append(f"Title: {title[0]}")

    # Abstract
    abstract = root.xpath("//tei:abstract//tei:p//text()", namespaces=ns)
    if abstract:
        sections.append("Abstract:\n" + " ".join(abstract))

    # Body
    body_paragraphs = root.xpath("//tei:body//tei:p//text()", namespaces=ns)
    if body_paragraphs:
        sections.append("Body:\n" + " ".join(body_paragraphs))

    return "\n\n".join(sections)