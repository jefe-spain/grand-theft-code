<h1 align="center">Grand Theft Code</h1>

<p align="center">
  Un tema animado de atardecer para <a href="https://t3.codes">T3 Code</a>. Tu agente lo instala con un solo mensaje.
</p>

<p align="center">
  <a href="https://jefe-spain.github.io/grand-theft-code/"><b>Demo en vivo</b></a> · <a href="README.md">English</a>
</p>

<p align="center">
  <img src="assets/mockup.svg" alt="Maqueta animada de T3 Code con el tema Grand Theft Code" width="100%">
</p>

<p align="center"><sub>Maqueta animada. Los hilos y mensajes que aparecen son inventados.</sub></p>

## Instalación

Pega esto en un hilo de T3 Code:

```text
Instala el tema Grand Theft Code para T3 Code:

1. Llama a t3_theme_read y toma themesDir del resultado.
2. Descarga https://raw.githubusercontent.com/jefe-spain/grand-theft-code/main/themes/grand-theft-code.json en esa carpeta, con el mismo nombre de fichero.
3. Llama a t3_theme_set con themeId "grand-theft-code" y appearance "light".
```

Para volver atrás, pide a tu agente un tema de serie, por ejemplo `t3-chat`.

<details>
<summary>Sin el logo VI</summary>
<br>

Usa `grand-theft-code-clean` en lugar de `grand-theft-code`, tanto en la URL como en el id del tema.

<img src="assets/preview-clean.png" alt="Grand Theft Code Clean en la página de demo">
</details>

<details>
<summary>Instalación manual</summary>
<br>

Descarga [`themes/grand-theft-code.json`](themes/grand-theft-code.json) en la carpeta de temas de T3 Code (`~/.t3/userdata/themes/` en macOS) y pide a tu agente que cambie al tema `grand-theft-code`.
</details>

## Qué incluye

- **Fondo animado** en un único SVG: palmeras que se mecen, nubes, un avión, una estrella fugaz y un logo VI flotante.
- **Toda la app con el mismo estilo:** chat, compositor, barra lateral, menús, barras de desplazamiento y colores del terminal.
- **Respeta el movimiento reducido:** las animaciones se paran si tu sistema lo pide.
- **[Monaspace Neon](https://monaspace.githubnext.com/)** si está instalada, la fuente monoespaciada del sistema si no.

Probado con T3 Code 0.1.10 en macOS. Los temas se aplican en las apps de escritorio y web, no en la móvil.

## Desarrollo

Los ficheros del tema se generan a partir de las fuentes de `src/`. Python 3.9 o superior, sin dependencias.

```sh
python3 build.py          # src/ -> themes/ y la página de demo
python3 tools/mockup.py   # la imagen animada de arriba
```

## Créditos

Homenaje hecho por fans, sin relación con Rockstar Games, Take-Two Interactive ni T3 Code. Grand Theft Auto es una marca de sus propietarios. El logo se dibujó para este proyecto y no contiene material del juego; su rótulo usa [Pricedown](https://typodermicfonts.com/pricedown/) de Typodermic Fonts, incluida como trazados.

Publicado bajo la [licencia MIT](LICENSE).
