import pywikibot

# Configurar el tiempo de espera entre ediciones a 1 segundo
pywikibot.config.put_throttle = 1


def get_english_interwiki(page):
    interwiki_links = page.iterlanglinks()
    for link in interwiki_links:
        if link.site.code == 'en':
            return link.title
    return None

def main():
    # Establecer el sitio
    site = pywikibot.Site('es')

    # Obtener todas las páginas en el espacio de nombres principal
    pages = site.allpages(namespace=0)

    for page in pages:
        # Verificar si ya existe {language info} en la página
        if "{{language info" in page.text:
            print(f"La página {page.title()} ya contiene información de idioma inglés, se omitió la edición.")
            continue

        # Obtener el enlace interwiki del idioma inglés
        english_value = get_english_interwiki(page)

        if english_value is not None:
            # Añadir el texto al final
            new_text = f"{page.text}\n{{{{language info|en={english_value}}}}}"

            # Actualizar la página
            page.text = new_text
            page.save("Añadiendo información sobre idioma (language info)")
            print(f"🎉 Se añadió la información sobre idiomas a la página {page.title()} 🎉")
        else:
            # Omitir si no se encuentra el enlace interwiki
            continue

if __name__ == "__main__":
    main()
