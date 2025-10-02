import polib  # type: ignore
import argostranslate.translate
import re


def translate_po_file(input_file, output_file, source_lang='en', target_lang='tr'):
    # Yüklü dilleri al
    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = next((lang for lang in installed_languages if lang.code == source_lang), None)
    to_lang = next((lang for lang in installed_languages if lang.code == target_lang), None)

    if not from_lang or not to_lang:
        raise Exception("İstenen dil yüklü değil")

    translation = from_lang.get_translation(to_lang)

    # PO dosyasını yükle
    po = polib.pofile(input_file)

    # Çevrilen satır sayacı
    translated_count = 0

    # Her bir entry için sadece msgstr'yi çevir
    for entry in po:
        if entry.msgstr.strip():  # Boş değilse
            original_text = entry.msgstr

            # {SÜSLÜ_PARANTEZ} ve [] KÖŞELİ PARANTEZ içindeki ifadeleri koruyalım
            placeholders = re.findall(r'(\{.*?\}|\[.*?\])', original_text)
            temp_text = re.sub(r'(\{.*?\}|\[.*?\])', 'PLACEHOLDER', original_text)

            # Çeviri yap
            translated_text = translation.translate(temp_text)

            # Geri yerine koy
            for placeholder in placeholders:
                translated_text = translated_text.replace("PLACEHOLDER", placeholder, 1)

            if translated_text != original_text:  # Çeviri yapıldıysa sayacı artır
                translated_count += 1

            entry.msgstr = translated_text
            print(f"Çevrildi: {original_text} -> {entry.msgstr}")

    # Çevrilen dosyayı kaydet
    po.save(output_file)
    print(f"\nToplam çevrilen satır sayısı: {translated_count}")
    print(f"Çevirilen dosya kaydedildi: {output_file}")


if __name__ == '__main__':
    translate_po_file('en.po', 'tr.po')
