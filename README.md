# Lex Puebla

Texto de las leyes vigentes del Estado Libre y Soberano de Puebla en Markdown, tomado de las versiones oficiales publicadas por el Orden Jurídico Poblano (ojp.puebla.gob.mx) y el Periódico Oficial del Estado de Puebla.

Complementa al repositorio de leyes federales Lex MX (https://github.com/ingteranalvarez/lex-mx) y sigue su mismo formato.

## Estructura

Cada ley es un archivo en `leyes/<CLAVE>.md` con un encabezado YAML:

```yaml
---
type: ley-estatal
estado: Puebla
sigla: CCPue
slug: CCPue
titulo: "Código Civil para el Estado Libre y Soberano de Puebla"
ultima_reforma: "AAAA-MM-DD"
fuente: "Orden Jurídico Poblano / Periódico Oficial del Estado de Puebla"
---
```

Los artículos inician con `**Artículo N.**` para facilitar su localización.

`catalog.json` contiene una entrada por ley con su clave, título y fecha de última reforma.

## Advertencia

Este repositorio no es una fuente oficial. Antes de fundar un escrito en un artículo, verifique su redacción y vigencia contra el Periódico Oficial del Estado de Puebla.
