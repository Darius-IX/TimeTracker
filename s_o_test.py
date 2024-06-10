from pypdf import PdfReader, PdfWriter
from pypdf.constants import AnnotationDictionaryAttributes


def q1():
    list_of_dicts = [{'name': 'Bob'},{'name': 'Alice'},{'name':'Jenny'}]
    list_2 = ['b', 'Alic']

    def contains_name(current_dict: dict) -> bool:
        current_name = current_dict["name"]
        for name_part in list_2:
            # true, if entry in list_2 is part of any name ignoring capitalization
            if name_part.lower() in current_name.lower():
            # use below if you want the names to match exactly
            # if name_part == current_name:
                return True
        return False

    result = filter(contains_name, list_of_dicts)
    print(list(result))


def q2():
    reader = PdfReader("RechnungTemplate1.pdf")
    writer = PdfWriter()
    writer.append(reader)
    fields = []
    for page in reader.pages:
        writer.reattach_fields(page)
        for annot in page.annotations:
            annot = annot.get_object()
            if annot[AnnotationDictionaryAttributes.Subtype] == "/Widget":
                fields.append(annot)
                if annot['/FT'] == "/Tx":
                    fieldName = annot["/T"]
                    writer.update_page_form_field_values(
                        writer.pages[page.page_number],
                        {fieldName: "Test"},
                        auto_regenerate=False,
                    )
    print(fields)


if __name__ == '__main__':
    q2()
